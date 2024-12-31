from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1)
}

schedule_interval = '*/10 * * * * *'

logger = logging.getLogger(__name__)

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

def create_dataframe(**kwargs):
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
    

with DAG('stream_user_data', default_args=default_args, schedule_interval=schedule_interval, catchup=False) as dag:
    fetch_user_data_task = PythonOperator(
        task_id='fetch_user_data',
        python_callable=fetch_user_data
    )

    create_dataframe_task = PythonOperator(
        task_id='create_dataframe',
        python_callable=create_dataframe
    )

    fetch_user_data_task >> create_dataframe_task