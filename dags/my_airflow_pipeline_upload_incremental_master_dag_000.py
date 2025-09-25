# my_airflow_pipeline_upload_incremental_master_dag_000.py
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

   
with DAG(
    dag_id = "my_airflow_pipeline_upload_incremental_master_dag_000", 
    start_date=datetime(2025, 9, 23), 
    schedule_interval=None, 
    catchup=False,
    tags=['my_airflow_upload_incremental']
) as dag:

    start = EmptyOperator(task_id='Start_of_the_incremental_upload_pipeline')

    t1 = TriggerDagRunOperator(
        task_id="my_airflow_110_upload_incremental",
        trigger_dag_id="my_airflow_110_upload_incremental"
    )

    start >> t1
