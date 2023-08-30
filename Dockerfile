FROM python:3.8

WORKDIR /work

COPY ./requirements.txt /work/requirements.txt

RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install -r requirements.txt