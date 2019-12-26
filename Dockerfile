FROM python:3.8.0-buster

ENV AIRFLOW_HOME /root/ airflow
WORKDIR $AIRFLOW_HOME
RUN apt-get update && apt-get install -y supervisor
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY config/airflow.cfg $AIRFLOW_HOME/airflow.cfg
COPY config/supervisord.conf /etc/supervisord.conf
RUN airflow initdb
CMD supervisord -c /etc/supervisord.conf
