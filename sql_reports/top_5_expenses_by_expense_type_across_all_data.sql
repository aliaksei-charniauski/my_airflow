-- Report Name: TOP-5 expenses by Expense Type across all data
--
-- Description: usage of DENSE_RANK analytical functions

WITH ds as
(
SELECT   
    SUBSTR('0' || cet.expense_type_id, -2) || '-' || cet.expense_type_name AS expense_type_name,
	re.note,
	re.amount,
	DENSE_RANK() OVER (PARTITION BY re.expense_type_id ORDER BY re.amount DESC) as dense_rank_amount
  FROM my_airflow.r_expense re
LEFT OUTER JOIN my_airflow.c_expense_type cet ON (cet.expense_type_id = re.expense_type_id)
)
SELECT DISTINCT
    ds.expense_type_name,
	ds.note,
	ds.amount,
	ds.dense_rank_amount
  FROM ds
 WHERE dense_rank_amount <= 5  
ORDER BY
    ds.expense_type_name,
    ds.dense_rank_amount
; 
