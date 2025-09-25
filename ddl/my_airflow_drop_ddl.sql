---===========================================================================---
-- SCHEMA: my_airflow
---===========================================================================---

---===========================================================================---
-- TABLES in correct orders:
---===========================================================================---
DROP TABLE IF EXISTS my_airflow.r_expense;
DROP TABLE IF EXISTS my_airflow.m_bank_coverage;
DROP TABLE IF EXISTS my_airflow.c_family;
DROP TABLE IF EXISTS my_airflow.c_expense_type;
DROP TABLE IF EXISTS my_airflow.c_currency_type;
DROP TABLE IF EXISTS my_airflow.c_bank;

---===========================================================================---
-- SEQUENCE in correct orders:
---===========================================================================---
DROP SEQUENCE IF EXISTS my_airflow.seq_r_expense;

---===========================================================================---
-- And finally the SCHEMA my_airflow
---===========================================================================---
DROP SCHEMA IF EXISTS my_airflow ;

---===========================================================================---
