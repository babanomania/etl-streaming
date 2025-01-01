from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from datetime import datetime, timedelta
import requests
import logging
import json

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1)
}

logger = logging.getLogger(__name__)

def load_connections():
    
    from airflow.models import Connection
    from airflow.utils import db

    db.merge_conn(
        Connection(
            conn_id="t1",
            conn_type="kafka",
            extra=json.dumps({"socket.timeout.ms": 10, "bootstrap.servers": "kafka-broker:29092"}),
        )
    )

def fetch_user_data(**kwargs):
    response = requests.get('http://generator:3000/api/user')
    if response.status_code == 200:
        user_data = response.json()

        task_instance = kwargs['ti']
        task_instance.xcom_push(key='user_data', value=user_data)

    else:
        error_msg = f"Failed to fetch user data. Status code: {response.status_code}"
        logger.error(error_msg)
        raise Exception(error_msg)

def parse_user_data(**kwargs):
    user_data = kwargs['ti'].xcom_pull(key='user_data', task_ids='fetch_user_data')
    logger.info(f"user_data: {user_data}")
    
    name_dict = user_data.get('results')[0]['name']
    name_attr = f"{name_dict['title']} {name_dict['first']} {name_dict['last']}"
    gender_attr = user_data.get('results')[0]['gender']
    age_attr = user_data.get('results')[0]['dob']['age']

    person_dict = {
        'name': name_attr,
        'gender': gender_attr,
        'age': age_attr
    }

    logger.info(f"Person: {person_dict}")

    task_instance = kwargs['ti']
    task_instance.xcom_push(key='person_dict', value=person_dict)

def produce_to_kafka(person_dict):
    if isinstance(person_dict, str):
        try:
            person_dict = json.loads(person_dict.replace("'", '"'))
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise
        
    yield ("person", json.dumps(person_dict))
    logger.info(f"Sent to Kafka: {person_dict}")

with DAG('stream_user_data', default_args=default_args, schedule_interval=timedelta(seconds=5), catchup=False) as dag:
    
    dag.max_active_runs = 5  # Allow 3 parallel runs
    
    load_connections_task = PythonOperator(
        task_id='load_connections',
        python_callable=load_connections,
        pool='default_pool'
    )
    
    fetch_user_data_task = PythonOperator(
        task_id='fetch_user_data',
        python_callable=fetch_user_data,
        pool_slots=1,  # Each task takes 1 slot
    )

    parse_user_data_task = PythonOperator(
        task_id='parse_user_data',
        python_callable=parse_user_data
    )

    produce_to_kafka_task = ProduceToTopicOperator(
        topic="{{ var.value.kafka_topic }}",
        kafka_config_id='t1',
        task_id='produce_to_kafka',
        producer_function=produce_to_kafka, 
        producer_function_args=["{{ ti.xcom_pull(key='person_dict', task_ids='parse_user_data') }}"],
    )

    load_connections_task >> fetch_user_data_task >> parse_user_data_task >> produce_to_kafka_task