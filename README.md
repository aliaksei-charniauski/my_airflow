# my_airflow
--------------------
Summary and Objectives: 
--------------------
This repository contains an project example of Python/Postgres code implementation to be orchestrated by Airflow.
The project is based on providing the support in the personal finance area and leveraged the management of family expenses.
This project repository is tarteged to represent the expertise in such areas as:
  - Database Development.
  - Datawarehouse Development.
  - Data Modelling.
  - SQL/ANSI SQL.
  - Postgres.
  - Python.
  - Airflow.

--------------------
Project description and details:
--------------------
Provided code is allow to perform the full schema deployment (for Postgres DB), 
i.e. a whole schema model creation with all tables, constraints, sequences etc.
with upload of the all initial data from csv-files 
and providing the ways to upload the incremental data from csv-file.
Also full rollback/delete of schema is included like a separate step.

Here is the structure of project:

/dags => contains all DAGs (Python) like individual, so combined into pipelines with multisteps for deployment, 
         upload or incremental upload.
/ddl => contains Postres DDL for deployment schema and drop schema.
/sql_reports => contains reports, produced by Postgres SQL queries.
/upload => contains CVS-files (initial data, and incremential ones) to perform upload into schema.
