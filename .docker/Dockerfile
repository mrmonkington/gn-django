FROM docker.gamer-network.net/python-node:3.6-6.17.0

ARG DOCKER_UID
ARG ENV=test
ARG FURY_AUTH

ENV ENV=${ENV}
ENV FURY_AUTH=$FURY_AUTH

RUN useradd -u ${DOCKER_UID} -ms /bin/bash app
RUN chmod -R 777 /home/app

ENV PYTHONUNBUFFERED 1
ADD . /code
WORKDIR /code
RUN chown -R app:app /code

USER app

RUN .docker/deploy/install_requirements.sh $ENV

EXPOSE 8000
ENTRYPOINT .docker/deploy/start.sh $ENV
