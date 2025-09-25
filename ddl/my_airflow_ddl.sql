---===========================================================================---
-- SCHEMA: my_airflow
---===========================================================================---

-- DROP SCHEMA IF EXISTS my_airflow ;

CREATE SCHEMA IF NOT EXISTS my_airflow;

---===========================================================================---
-- SEQUENCE: my_airflow.seq_r_expense
---===========================================================================---

-- DROP SEQUENCE IF EXISTS my_airflow.seq_r_expense;

CREATE SEQUENCE IF NOT EXISTS my_airflow.seq_r_expense
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 9223372036854775807
    CACHE 1;

ALTER SEQUENCE IF EXISTS my_airflow.seq_r_expense
    OWNER TO postgres;

---===========================================================================---
-- Table: my_airflow.c_bank
---===========================================================================---

-- DROP TABLE IF EXISTS my_airflow.c_bank;

CREATE TABLE IF NOT EXISTS my_airflow.c_bank
(
    bank_id numeric(12) NOT NULL,
    bank_name character varying(256) NOT NULL,
    note character varying(256),
    CONSTRAINT c_bank_pkey PRIMARY KEY (bank_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS my_airflow.c_bank
    OWNER to postgres;
-- Index: xpk_c_bank

-- DROP INDEX IF EXISTS my_airflow.xpk_c_bank;

CREATE UNIQUE INDEX IF NOT EXISTS xpk_c_bank
    ON my_airflow.c_bank
    (bank_id ASC)
    TABLESPACE pg_default;

---===========================================================================---
-- Table: my_airflow.c_currency_type
---===========================================================================---

-- DROP TABLE IF EXISTS my_airflow.c_currency_type;

CREATE TABLE IF NOT EXISTS my_airflow.c_currency_type
(
    currency_id numeric(12) NOT NULL,
    currency_name character varying(256) NOT NULL,
    CONSTRAINT c_currency_type_pkey PRIMARY KEY (currency_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS my_airflow.c_currency_type
    OWNER to postgres;
-- Index: xpk_c_currency_type

-- DROP INDEX IF EXISTS my_airflow.xpk_c_currency_type;

CREATE UNIQUE INDEX IF NOT EXISTS xpk_c_currency_type
    ON my_airflow.c_currency_type
    (currency_id ASC)
    TABLESPACE pg_default;

---===========================================================================---
-- Table: my_airflow.c_expense_type
---===========================================================================---

-- DROP TABLE IF EXISTS my_airflow.c_expense_type;

CREATE TABLE IF NOT EXISTS my_airflow.c_expense_type
(
    expense_type_id numeric(12) NOT NULL,
    expense_type_name character varying(256) NOT NULL,
    CONSTRAINT c_expense_type_pkey PRIMARY KEY (expense_type_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS my_airflow.c_expense_type
    OWNER to postgres;
-- Index: xpk_c_expense_type

-- DROP INDEX IF EXISTS my_airflow.xpk_c_expense_type;

CREATE UNIQUE INDEX IF NOT EXISTS xpk_c_expense_type
    ON my_airflow.c_expense_type
    (expense_type_id ASC)
    TABLESPACE pg_default;

---===========================================================================---
-- Table: my_airflow.c_family
---===========================================================================---

-- DROP TABLE IF EXISTS my_airflow.c_family;

CREATE TABLE IF NOT EXISTS my_airflow.c_family
(
    family_id numeric(12) NOT NULL,
    family_name character varying(256) NOT NULL,
    CONSTRAINT c_family_pkey PRIMARY KEY (family_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS my_airflow.c_family
    OWNER to postgres;
-- Index: xpk_c_family

-- DROP INDEX IF EXISTS my_airflow.xpk_c_family;

CREATE UNIQUE INDEX IF NOT EXISTS xpk_c_family
    ON my_airflow.c_family
    (family_id ASC)
    TABLESPACE pg_default;


---===========================================================================---
-- Table: my_airflow.m_bank_coverage
---===========================================================================---


-- DROP TABLE IF EXISTS my_airflow.m_bank_coverage;

CREATE TABLE IF NOT EXISTS my_airflow.m_bank_coverage
(
    bank_coverage_id numeric(12) NOT NULL,
    bank_id numeric(12),
    coverage_name character varying(256) NOT NULL,
    CONSTRAINT m_bank_coverage_pkey PRIMARY KEY (bank_coverage_id),
    CONSTRAINT fk_bank_coverage_ref_bank FOREIGN KEY (bank_id) REFERENCES my_airflow.c_bank (bank_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS my_airflow.m_bank_coverage
    OWNER to postgres;
-- Index: xpk_m_bank_coverage

-- DROP INDEX IF EXISTS my_airflow.xpk_m_bank_coverage;

CREATE UNIQUE INDEX IF NOT EXISTS xpk_m_bank_coverage
    ON my_airflow.m_bank_coverage
    (bank_coverage_id ASC)
    TABLESPACE pg_default;


---===========================================================================---
-- Table: my_airflow.r_expense
---===========================================================================---


-- DROP TABLE IF EXISTS my_airflow.r_expense;

CREATE TABLE IF NOT EXISTS my_airflow.r_expense
(
    expense_id numeric(12) NOT NULL DEFAULT nextval('my_airflow.seq_r_expense'::regclass),
    expense_date date,
    expense_type_id numeric(12),
    expense_sub_type_id character varying(256),
    currency_id numeric(12),
    amount numeric(12,2),
    family_id numeric(12),
    note character varying(256),
    row_hash  character varying(32),
    CONSTRAINT r_expense_pkey PRIMARY KEY (expense_id),
    CONSTRAINT r_expense_ukey UNIQUE (row_hash),
    CONSTRAINT fk_expense_ref_currency_type FOREIGN KEY (currency_id) REFERENCES my_airflow.c_currency_type (currency_id),
    CONSTRAINT fk_expense_ref_expense_type FOREIGN KEY (expense_type_id) REFERENCES my_airflow.c_expense_type (expense_type_id),
    CONSTRAINT fk_expense_ref_family FOREIGN KEY (family_id) REFERENCES my_airflow.c_family (family_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS my_airflow.r_expense
    OWNER to postgres;
-- Index: xpk_r_expense

-- DROP INDEX IF EXISTS my_airflow.xpk_r_expense;

CREATE UNIQUE INDEX IF NOT EXISTS xpk_r_expense
    ON my_airflow.r_expense
    (expense_id ASC)
    TABLESPACE pg_default;

-- DROP INDEX IF EXISTS my_airflow.xuk_r_expense;

CREATE UNIQUE INDEX IF NOT EXISTS xuk_r_expense
    ON my_airflow.r_expense
    (row_hash ASC)
    TABLESPACE pg_default;


---===========================================================================---
