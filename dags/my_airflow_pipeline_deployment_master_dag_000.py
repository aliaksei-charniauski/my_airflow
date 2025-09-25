# my_airflow_pipeline_deployment_master_dag_000.py
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

   
with DAG(
    dag_id = "my_airflow_pipeline_deployment_master_dag_000", 
    start_date=datetime(2025, 9, 23), 
    schedule_interval=None, 
    catchup=False,
    tags=['my_airflow_deployment']
) as dag:

    start = EmptyOperator(task_id='Start_of_the_whole_deployment_pipeline')

    t1 = TriggerDagRunOperator(
        task_id="my_airflow_001_deployment",
        trigger_dag_id="my_airflow_001_deployment",
        wait_for_completion=True,
        reset_dag_run=True
    )

    t2 = TriggerDagRunOperator(
        task_id="my_airflow_100_upload",
        trigger_dag_id="my_airflow_100_upload",
        wait_for_completion=True,
        reset_dag_run=True
    )

    t3 = TriggerDagRunOperator(
        task_id="my_airflow_110_upload_incremental",
        trigger_dag_id="my_airflow_110_upload_incremental",
    )

    start >> t1 >> t2 >> t3
    