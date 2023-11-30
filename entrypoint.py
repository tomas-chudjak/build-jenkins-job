#!/usr/bin/env python3

# use of https://python-jenkins.readthedocs.io/en/latest/index.html

import os
import sys
import requests
import jenkins
import time
import json


def mandatory_arg(argv):
    if argv == "":
        raise ValueError("Only job_params can be empty. Required fields: url, token, user and path")
    return argv


# mandatory
JENKINS_URL = mandatory_arg(sys.argv[1])
JENKINS_TOKEN = mandatory_arg(sys.argv[2])
JENKINS_USER = mandatory_arg(sys.argv[3])
JOB_PATH = mandatory_arg(sys.argv[4])
JENKINS_PORT = mandatory_arg(sys.argv[5])

# not mandatory
JOB_PARAMS = sys.argv[6] or '{}'
IS_SECURE = sys.argv[7] or False

# create/connect jenkins server
if IS_SECURE:
    server_url = f"https://{JENKINS_URL}:{str(JENKINS_PORT)}"
else:
    server_url = f"http://{JENKINS_URL}:{str(JENKINS_PORT)}"

print(f"Server URL: {server_url}")
server = jenkins.Jenkins(server_url, username=JENKINS_USER, password=JENKINS_TOKEN)

user = server.get_whoami()
version = server.get_version()
print(f"Hello {user['fullName']} from Jenkins {version}")

def build_job_with_retry(server, job_name, parameters, token, max_retries=3, delay=5):
    attempt = 0
    while attempt < max_retries:
        try:
            server.build_job(job_name, parameters=parameters, token=token)
            return  # Successful build job
        except requests.exceptions.RequestException as e:
            print(f"Error on attempt {attempt + 1}: {e}")
            time.sleep(delay)
            attempt += 1
    raise Exception("Failed to build job after several attempts")

# build job
split = JOB_PATH.split("job/")
job_name = "".join(split)
# server.build_job(job_name, parameters=json.loads(JOB_PARAMS), token=JENKINS_TOKEN)
try:
    build_job_with_retry(server, job_name, parameters=json.loads(JOB_PARAMS), token=JENKINS_TOKEN)
except Exception as e:
    print(f"Failed to start Jenkins job: {e}")
    sys.exit(1)
queue_info = server.get_queue_info()
queue_id = queue_info[0].get('id')

# define url to request build_number

if IS_SECURE:
    url = f"https://{JENKINS_USER}:{JENKINS_TOKEN}@{JENKINS_URL}:{JENKINS_PORT}/queue/item/{queue_id}/api/json?pretty=true"
else:
    url = f"http://{JENKINS_USER}:{JENKINS_TOKEN}@{JENKINS_URL}:{JENKINS_PORT}/queue/item/{queue_id}/api/json?pretty=true"


def get_trigger_info(url: str):
    trigger_info = requests.get(url).json()
    return trigger_info


while "executable" not in (info := get_trigger_info(url)):
    time.sleep(6)

print(info)

build_number = info["executable"]["number"]
print(f"BUILD NUMBER: {build_number}")

def set_output(name, value):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'{name}={value}', file=fh)

def get_status(server, name: str, number: int, max_retries=3, delay=5) -> str:
    attempt = 0
    while attempt < max_retries:
        try:
            build_info = server.get_build_info(name=job_name, number=number)
            if build_info and build_info.get("result") is not None:
                set_output("job_url", build_info["url"])
                return build_info["result"]
            else:
                raise ValueError("Empty response or missing 'result' in build info")
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Retry {attempt + 1}/{max_retries} for job status due to error: {e}")
            time.sleep(delay)
            attempt += 1
    raise Exception("Failed to retrieve job status after several attempts")

    # build_info = server.get_build_info(name=name, number=number)
    # set_output("job_url", build_info["url"])
    # job_status = build_info["result"]
    # return job_status

try:
    status = get_status(server, job_name, build_number)
except Exception as e:
    print(f"Failed to retrieve job status: {e}")
    sys.exit(1)


# while not (status := get_status(job_name, build_number)):
#     time.sleep(1)

print(f"Job status is : {status}")
# print(f"::set-output name=job_status::{status}")

set_output("status", status)

if status != 'SUCCESS':
    exit(1)
