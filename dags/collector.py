import os
import boto3
from airflow import DAG
from airflow.contrib.operators.ecs_operator import ECSOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 12, 24),
    'email': ['airflow@example.com'],
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

client = boto3.client(
    service_name="ecs",
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name="us-west-1",
)

dag = DAG('collector', default_args=default_args, schedule_interval=timedelta(days=1))

task_definition = "taskdef-airflow-test-dev-aece9bcd"
cluster = "cluster-airflow-test-dev"
overrides = {
    'containerOverrides': [{
        'name': 'alpine',
        'command': ['sleep', '60'],
    }]
}

t1 = ECSOperator(
    task_id="run_collector",
    dag=dag,
    task_definition=task_definition,
    cluster=cluster,
    overrides=overrides,
    region_name="us-west-1",
)
# t2 = ECSOperator(
#     task_id='sleep',
#     bash_command='sleep 5',
#     retries=3,
#     dag=dag)
#
# templated_command = """
#     {% for i in range(5) %}
#         echo "{{ ds }}"
#         echo "{{ macros.ds_add(ds, 7)}}"
#         echo "{{ params.my_param }}"
#     {% endfor %}
# """
#
# t3 = ECSOperator(
#     task_id='templated',
#     bash_command=templated_command,
#     params={'my_param': 'Parameter I passed in'},
#     dag=dag)
#
# t2.set_upstream(t1)
# t3.set_upstream(t1)
