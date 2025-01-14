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

# build job
split = JOB_PATH.split("job/")
job_name = "".join(split)
server.build_job(job_name, parameters=json.loads(JOB_PARAMS), token=JENKINS_TOKEN)
queue_info = server.get_queue_info()
queue_id = queue_info[0].get('id')

# define url to request build_number

if IS_SECURE:
    url = f"https://{JENKINS_USER}:{JENKINS_TOKEN}@{JENKINS_URL}:{JENKINS_PORT}/queue/item/{queue_id}/api/json?pretty=true"
else:
    url = f"http://{JENKINS_USER}:{JENKINS_TOKEN}@{JENKINS_URL}:{JENKINS_PORT}/queue/item/{queue_id}/api/json?pretty=true"

print(f"URL:  {url}")

# def get_trigger_info(url: str):
#     try:
#         response = requests.get(url, timeout=120)  # Set a reasonable timeout
#         response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
#         return response.json()
#     except requests.RequestException as e:
#         print(f"HTTP Request failed: {e}")
#         return None
    
# max_retries = 60  # Maximum number of retries
# sleep_timeout = 10 # Sleep timeout between the HTTP requests
# attempts = 0

# while True:
#     info = get_trigger_info(url)
#     if info is not None and "executable" in info:
#         break

#     attempts += 1
#     if attempts >= max_retries:
#         print("Maximum retries reached. Exiting.")
#         exit()

#     time.sleep(sleep_timeout)

# print(info)
# if "number" in info["executable"]:
#     build_number = info["executable"]["number"]
#     print(f"Build number: {build_number}")
# else:
#     print("The 'number' key is not present in the 'executable' dictionary.")

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

def get_status(name: str, number: int) -> str:
    build_info = server.get_build_info(name=name, number=number)
    set_output("job_url", build_info["url"])
    job_status = build_info["result"]
    return job_status


while not (status := get_status(job_name, build_number)):
    time.sleep(3)

print(f"Job status is : {status}")
# print(f"::set-output name=job_status::{status}")

set_output("status", status)

if status != 'SUCCESS':
    exit(1)
