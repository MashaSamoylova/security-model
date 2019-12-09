FROM ubuntu:latest

RUN apt update && apt install -y python3 python3-pip libmysqlclient-dev libssl-dev libcrypto++-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]