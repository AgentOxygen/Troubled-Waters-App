# syntax=docker/dockerfile:1
RUN apt-get update -y --fix-missing && apt-get install -y python3.6
RUN apt-get -y install python3-pip

COPY . /app ?
WORKDIR ../app ? 

ENV LC_CTYPE=en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]