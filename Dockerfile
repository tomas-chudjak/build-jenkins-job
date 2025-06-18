FROM 270171913989.dkr.ecr.us-west-2.amazonaws.com/hostaway:python-3.13

COPY entrypoint.py /entrypoint.py

RUN chmod +x /entrypoint.py

WORKDIR /

ENTRYPOINT ["/entrypoint.py"]