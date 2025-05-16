# Container image that runs your code
# FROM python:3.8

# #install pre-requisites
# RUN apt-get update

# RUN pip install --upgrade pip

# # Copies your code file from your action repository to the filesystem path `/` of the container
# COPY entrypoint.py /entrypoint.py
# COPY requirements.txt /requirements.txt

# RUN chmod +x /entrypoint.py

# WORKDIR /

# RUN pip install -r requirements.txt

# # Code file to execute when the docker container starts up (`entrypoint.py`)
# ENTRYPOINT ["/entrypoint.py"]

FROM 270171913989.dkr.ecr.us-west-2.amazonaws.com/hostaway:python-3.8

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.py /entrypoint.py
# COPY requirements.txt /requirements.txt

RUN chmod +x /entrypoint.py

WORKDIR /

# RUN pip install -r requirements.txt

# Code file to execute when the docker container starts up (`entrypoint.py`)
ENTRYPOINT ["/entrypoint.py"]