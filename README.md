# my_airflow
This repository contains an project example of Python/Postgres code to be orchestrated by Airflow.
The project is targeted to support the personal finance area and leveraged the management of family expenses.
The goal of storing such data is to produce financial reports and querying of any other expenses-related information.

Provided code is allow to perform the full schema deployment (Postgres), i.e. whole schema model creation with all tables, constraints, sequences etc.
with upload of the all initial data from csv-files 
and providing the ways to upload the incremental data from csv-file.
Also full rollback/delete of schema is included like a separate step.

Here is the structure of project:
/dags => contains all DAGs (Python) like individual, so combined into multisteps
/ddl => contains Postres DDL for deployment schema and drop schema.
/upload => contains CVS-files (initial data, and incremential ones) to perform upload into schema.
