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

ecs = boto3.client(
    service_name="ecs",
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name="us-west-1",
)

# DAG作成
dag = DAG('collector', default_args=default_args, schedule_interval=timedelta(days=1))

# ECS task定義
task_definition = "airflow-test-dev"
cluster = "cluster-airflow-test-dev"
overrides = {
    'containerOverrides': [{
        'name': 'alpine',
        'command': ['sleep', '60'],
    }]
}

# default sessionにregionは保存されない？
ec2 = boto3.client(
    service_name='ec2',
    region_name="us-west-1",
)
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_subnets
subnets = ec2.describe_subnets(Filters=[
    {
        "Name": "vpc-id",
        "Values": [
            os.environ['VPC_ID'],
        ]
    }
])['Subnets']
subnet_ids = list(map(lambda subnet: subnet['SubnetId'], subnets))

network_configuration = {
    "awsvpcConfiguration": {
        "subnets": subnet_ids,
        "securityGroups": ["sg-07381accdf2c5b195"],

        "assignPublicIp": "ENABLED",
    }
}

# Operator作成

t1 = ECSOperator(
    task_id="run_collector",
    dag=dag,
    task_definition=task_definition,
    cluster=cluster,
    overrides=overrides,
    region_name="us-west-1",
    launch_type="FARGATE",
    network_configuration=network_configuration,
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
