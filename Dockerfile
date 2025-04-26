
FROM python:3.13 as python-base

ENV CODE_DIR=/opt/project

RUN mkdir -p $CODE_DIR

COPY . $CODE_DIR
WORKDIR $CODE_DIR

RUN python -m pip --no-cache-dir install --upgrade pip && \
    python -m pip --no-cache-dir install -r requirements.txt

VOLUME /opt/project/media
VOLUME /opt/project/static

ENTRYPOINT ["/opt/project/entrypoint.sh"]
