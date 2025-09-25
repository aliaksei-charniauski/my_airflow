# Project: my_airflow
# DAG: my_airflow_900_drop
#
# Date: 2025_09_17
#
# Description: 
# Full schema clean-up and drop. Schema will be dropped as well.

import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import hashlib
import psycopg2
from psycopg2.extras import execute_values

# --- CONFIGURATION ---
# !!! This path should be added to docker-compose.yaml !!!
APP_PATH = "/app/data/ddl"

DB_CONFIG = {
#    "host": "localhost",
    "host": "host.docker.internal",
    "port": 5432,
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres"
}

APP_SCHEMA = 'my_airflow'

# --- CONFIGURATION ---

def get_ddl_files(my_ddl_dir):

    print("Obtaining files from %s" % (my_ddl_dir))

    # Get list of filenames (excluding subdirectories)
    ddl_filenames = [f for f in os.listdir(my_ddl_dir) if os.path.isfile(os.path.join(my_ddl_dir, f)) and f.startswith('my_airflow_drop_ddl') and f.endswith('.sql')]

    print(ddl_filenames)
    
    return ddl_filenames

####### --- START OF MAIN PROCESS --- ######
    
def load_ddl_file(ddl_filepath):
    """Read DDL file"""
    print("Extracting data from %s" % (ddl_filepath))

    # Read the file
    with open(ddl_filepath, 'r') as file:
        ddl_content = file.read()
    
    return ddl_content


def ddl_execution(ddl_content):
    """DDL file execution"""

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Execute the DDL
    cur.execute(ddl_content)
    conn.commit()

    cur.close()
    conn.close()

    print("DDL Execution complete")


def my_airflow_900_drop():
    
    now = datetime.now()
    print(">>> START OF PROCESS %s: %s <<<" % ('my_airflow_900_drop', now))
    
###########################################
    print(">>> Configuration <<<")
    print("CWD:", os.getcwd())
    print("Mounted files in directories:")

    print("/opt/airflow/dags => %s" % (os.listdir("/opt/airflow/dags")))
    print("/opt/airflow/logs => %s" % (os.listdir("/opt/airflow/logs")))
    print("/opt/airflow/config => %s" % (os.listdir("/opt/airflow/config")))
    print("/opt/airflow/plugins => %s" % (os.listdir("/opt/airflow/plugins")))
### These are mine:
    print("/app/data/ddl => %s" % (os.listdir("/app/data/ddl")))
###########################################
    
    # gather ddl files to upload
    print(">>> Entry point: get_ddl_files(APP_PATH) <<<")
    ddl_filenames = get_ddl_files(APP_PATH)
    
    for filename in ddl_filenames:
        # load ddl file
        print(">>> Entry point: filename => load_ddl_file(APP_PATH + '/' + filename) <<<")
        ddl_content = load_ddl_file(APP_PATH + '/' + filename)
        
        # ddl file execution
        print(">>> Entry point: filename => ddl_execution(ddl_content) <<<")
        ddl_execution(ddl_content)

    now = datetime.now()
    print(">>> END OF PROCESS %s: %s <<<" % ('my_airflow_900_drop', now))

####################################################################################
# Define the DAG
default_dag_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 15),
}

with DAG(
    'my_airflow_900_drop',
    default_args=default_dag_args,
    schedule_interval=None,  # or None for manual runs
    catchup=False,
) as dag:

    task_upload = PythonOperator(
        task_id='my_airflow_900_drop',
        python_callable=my_airflow_900_drop
    )

    task_upload
    