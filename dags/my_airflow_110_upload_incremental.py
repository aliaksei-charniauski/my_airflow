# Project: my_airflow
# DAG: my_airflow_110_upload_incremental
#
# Date: 2025_09_24
#
# Description: 
# Initial DML Upload of CSV-files for my_airflow schema in Postgres

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
APP_PATH = "/app/data/upload"

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

def get_csv_files(my_upload_dir):

    print("Obtaining files from %s" % (my_upload_dir))

    # Get list of filenames (excluding subdirectories)
    cvs_filenames = [f for f in os.listdir(my_upload_dir) if os.path.isfile(os.path.join(my_upload_dir, f)) and f.endswith('.csv')]

    print(cvs_filenames)
    
    return cvs_filenames

####### --- START OF MAIN PROCESS --- ######
    
def extract_from_csv(filepath):
    """Read CSV file into DataFrame."""
    print("Extracting data from %s" % (filepath))
    return pd.read_csv(filepath)



def transform_data(df, filename):
    """Clean and transform data."""
    print("Transforming data for %s" % (filename))

    table_name, ext = filename.rsplit('.', 1)
    table_name = table_name.replace("_data", "")

    # drop all columns which are based on sequence
    if (table_name == 'r_expense') and ('expense_id)' in df.columns):
        df.drop(columns=['expense_id'], inplace=True)

    all_cnt = len(df)
    print("Total records for transformation = %s" % (all_cnt))

    # check whole df by nulls and replace them by 'NA'
    all_null_cnt = df.isnull().sum().sum()
    print("All NULLs cnt: %s" % (all_null_cnt))

    if all_null_cnt > 0:
        df.fillna('NA', inplace=True)

    return df


def calculate_hash(*values):
    # Convert values to strings, handle None, and use a delimiter
    combined = '|'.join(str(v) if v is not None else '' for v in values)
    return hashlib.md5(combined.encode('utf-8')).hexdigest()


def load_to_postgres(df, filename):
    """Load transformed data into PostgreSQL."""

    table_name, ext = filename.rsplit('.', 1)
    
    table_name = table_name.replace("_data", "")
    print(f"Inserting data into PostgreSQL table `{table_name}`...")
    
# added logic to redefine incremental filenames into filenames for regular tables (to remove "incremental" wording)
    if table_name == 'r_expense_incremental':
        table_name = table_name.replace("_incremental", "")
    
# major logic to prepare data    
    if table_name == 'r_expense':

        insert_query = f"""
            INSERT INTO {APP_SCHEMA}.{table_name} (expense_date, expense_type_id, expense_sub_type_id, currency_id, amount, family_id, note, row_hash)
            VALUES %s
            ON CONFLICT (row_hash) DO NOTHING
        """

        data_tuples = [
            (row['expense_date'], row['expense_type_id'], row['expense_sub_type_id'], row['currency_id'], row['amount'], row['family_id'], row['note'],\
             calculate_hash(row['expense_date'], row['expense_type_id'], row['expense_sub_type_id'], row['currency_id'], row['amount'], row['family_id'], row['note']))

            for _, row in df.iterrows()
        ]

    else:
        insert_query = None
    
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    if insert_query:
        
        execute_values(cur, insert_query, data_tuples)
        conn.commit()
        
        check_query = f"""
            SELECT COUNT(*) as cnt FROM {APP_SCHEMA}.{table_name}
        """

# Check and calculate the quantity of records in table 
        with conn.cursor() as cur:
            # Compose SQL safely with sql.Identifier to prevent SQL injection
#            query = sql.SQL("SELECT COUNT(*) as cnt FROM {}.{}").format(
#                sql.Identifier(APP_SCHEMA),
#                sql.Identifier(table_name)
#            )

            check_query = f"""
                SELECT COUNT(*) as cnt FROM {APP_SCHEMA}.{table_name}
            """
        
            cur.execute(check_query)
        
            # Fetch result
            result = cur.fetchone()
            total_count = result[0]  # or result['cnt'] if using cursor with dict output

            print(f"Total record count in {table_name} table = {total_count}")
        
    else:
        print(f"Warning: There is NO section defined to process `{filename}` file!")
        total_count = 0 
    
    cur.close()
    conn.close()

    print("Load complete")

    return total_count

def my_airflow_110_upload_incremental():
    

    now = datetime.now()
    print(">>> START OF PROCESS %s: %s <<<" % ('my_airflow_110_upload_incremental', now))
    
###########################################
### Check Mounted Volumes
    print(">>> Configuration <<<")
    print("CWD:", os.getcwd())
    print("Mounted files in directories:")

    print("/opt/airflow/dags => %s" % (os.listdir("/opt/airflow/dags")))
    print("/opt/airflow/logs => %s" % (os.listdir("/opt/airflow/logs")))
    print("/opt/airflow/config => %s" % (os.listdir("/opt/airflow/config")))
    print("/opt/airflow/plugins => %s" % (os.listdir("/opt/airflow/plugins")))
### These are mine:
    print("/app/data/upload => %s" % (os.listdir("/app/data/upload")))
###########################################
    
    # gather csv files to upload
    print(">>> Entry point: get_csv_files(APP_PATH) <<<")
    upload_filenames = get_csv_files(APP_PATH)
    
    for filename in upload_filenames:
        # load from csv
        print(">>> Entry point: filename => extract_from_csv(APP_PATH + '/' + filename) <<<")
        df_raw = extract_from_csv(APP_PATH + '/' + filename)
        
        # cleaning up
        print(">>> Entry point: filename => transform_data(df_raw, filename) <<<")
        df_clean = transform_data(df_raw, filename)
        
        # load to table
        print(">>> Entry point: filename => load_to_postgres(df_clean, filename) <<<")
        result = load_to_postgres(df_clean, filename)

    now = datetime.now()
    print(">>> END OF PROCESS %s: %s <<<" % ('my_airflow_110_upload_incremental', now))

####### --- END OF MAIN PROCESS --- ######


# Define the DAG
default_dag_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 9, 12),
}

with DAG(
    'my_airflow_110_upload_incremental',
    default_args=default_dag_args,
#    schedule_interval='@daily',  # or None for manual runs
    schedule_interval=None,  # or None for manual runs
    catchup=False,
) as dag:

    task_upload = PythonOperator(
        task_id='my_airflow_110_upload_incremental',
        python_callable=my_airflow_110_upload_incremental
    )

    task_upload
    