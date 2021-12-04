FROM alpine:edge

# Add project source
WORKDIR /usr/src/soundbot
COPY . ./

RUN apk update \
&& apk add --no-cache \
  ca-certificates \
  ffmpeg \
  opus \
  python3 \
  libsodium-dev \
\
# Install build dependencies
&& apk add --no-cache --virtual .build-deps \
  gcc \
  git \
  libffi-dev \
  make \
  musl-dev \
  python3-dev \
\

# Install pip dependencies
&& pip3 install --no-cache-dir -r requirements.txt \

# Clean up build dependencies
&& apk del .build-deps

VOLUME /usr/src/soundbot/config
VOLUME /usr/src/soundbot/clips

ENV APP_ENV=docker

ENTRYPOINT ["python3", "dockerentry.py"]