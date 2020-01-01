FROM python:3.7.4-buster

ENV AIRFLOW_HOME /root/airflow
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
WORKDIR $AIRFLOW_HOME
RUN apt-get update && apt-get install -y default-libmysqlclient-dev supervisor netcat
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY config/airflow.cfg $AIRFLOW_HOME/airflow.cfg
COPY dags $AIRFLOW_HOME/dags
