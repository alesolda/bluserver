FROM python:3.6.6-alpine3.8

# RUN apk update && \
#     apk upgrade && \
#     apk add \
#     rsyslog

ARG MY_UID
ARG MY_GID
ARG MY_UNAME

RUN adduser --disabled-password --gecos '' ${MY_UNAME} -u ${MY_UID} -g ${MY_GID}

USER ${MY_UNAME}

WORKDIR /src

ENTRYPOINT []

CMD ["./docker_init_server.sh"]
