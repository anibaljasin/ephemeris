FROM python:3.6-alpine3.11

RUN apk update
RUN apk add --no-cache bash

WORKDIR /usr/src/app
EXPOSE 4000
COPY . ephemeris
RUN pip install -r ephemeris/requirements.txt
ENTRYPOINT ["python", "ephemeris/app.py"]
