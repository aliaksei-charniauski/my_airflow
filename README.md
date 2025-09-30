# my_airflow
-----------------------
Summary and Objectives: 
-----------------------
This repository contains an project example of Python/Postgres code implementation to be orchestrated by Airflow.
The project is based on providing the support in the personal finance area and leveraged the management of family expenses.
This project repository is targeted to represent the expertise in such areas as:
  - Database Development.
  - Datawarehouse Development.
  - Data Modelling.
  - SQL/ANSI SQL.
  - Postgres.
  - Python.
  - Airflow.

--------------------------------
Project description and details:
--------------------------------
Provided code is allow to perform the full schema deployment (for Postgres DB), 
i.e. a whole schema model creation with all tables, constraints, sequences etc.
with upload of the all initial data from csv-files 
and providing the ways to upload the incremental data from csv-file.
Also full rollback/delete of schema is included like a separate step.

Here is the structure of project folders:

(1) /dags => contains all DAGs (Python) like individual, so combined into pipelines with multistep for deployment, 
upload or incremental upload.
All multistep pipelines have postfixes as "_master_dag_000.py".
All individual DAGs have no "_master_dag_"-wording inside their names.

(2) /ddl => contains Postres DDL for deployment schema and drop schema.

(3) /sql_reports => contains reports, produced by Postgres SQL queries.

(4) /upload => contains CVS-files (initial data, and incremental ones) to perform upload into schema.

--------------------------------
