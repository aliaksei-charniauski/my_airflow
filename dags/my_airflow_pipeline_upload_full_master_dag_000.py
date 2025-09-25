# my_airflow_pipeline_upload_full_master_dag_000.py
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

   
with DAG(
    dag_id = "my_airflow_pipeline_upload_full_master_dag_000", 
    start_date=datetime(2025, 9, 23), 
    schedule_interval=None, 
    catchup=False,
    tags=['my_airflow_upload_full']
) as dag:

    start = EmptyOperator(task_id='Start_of_the_full_upload_pipeline')

    t1 = TriggerDagRunOperator(
        task_id="my_airflow_100_upload",
        trigger_dag_id="my_airflow_100_upload"
    )

    start >> t1
