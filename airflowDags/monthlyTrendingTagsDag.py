from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from utilFunctions.stackoverflowQuery import get_top_trending_tags
from utilFunctions.s3Functions import upload_data_in_s3

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 7, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


MonthlyTrendingTagsDag = DAG(
    'MonthlyTrendingTagsDag',
    default_args=default_args,
    schedule_interval="00 23 28 * *",  
)


task_one = PythonOperator(
    task_id='getting_data_from_api',
    python_callable=get_top_trending_tags,
    do_xcom_push=True,
    dag=MonthlyTrendingTagsDag
)

task_two = PythonOperator(
    task_id='uploading_data_to_s3',
    python_callable=upload_data_in_s3,
    provide_context=True,
    dag=MonthlyTrendingTagsDag
)

task_one >> task_two
