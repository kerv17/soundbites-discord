FROM python:3.8-alpine


# Add project source
WORKDIR /usr/src/soundbot
COPY . ./

RUN apk update && apk add --no-cache --virtual .build-deps \
  build-base \
  libffi-dev \
  libsodium-dev

# Install dependencies
RUN apk update && apk add --no-cache \
  ca-certificates \
  ffmpeg \
  opus-dev \
  libffi \
  libsodium \
  gcc

# Install pip dependencies
RUN pip3 install --no-cache-dir -r requirements.txt


# Clean up build dependencies
RUN apk del .build-deps

VOLUME ["/usr/src/soundbot/config","/usr/src/soundbot/clips"]

ENV APP_ENV=docker

ENTRYPOINT ["python3", "dockerentry.py"]