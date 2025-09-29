-- Report Name: analysis of monthly expenses by Expense Type with comparison by previous and next months
--
-- Description: usage of LEAD/LAD analytical functions

WITH ds AS (
SELECT   
    SUBSTR('0' || cet.expense_type_id, -2) || '-' || cet.expense_type_name AS expense_type_name,
    COALESCE(TO_CHAR(re.expense_date, 'YYYY'), 'No Data') AS curr_year,
    COALESCE(TO_CHAR(re.expense_date, 'MM'), 'No Data') AS curr_month,
    COALESCE(SUM(re.amount),0) AS curr_monthly_amount
  FROM my_airflow.c_expense_type cet
LEFT OUTER JOIN my_airflow.r_expense re ON (re.expense_type_id = cet.expense_type_id)
GROUP BY 
       SUBSTR('0' || cet.expense_type_id, -2) || '-' || cet.expense_type_name,
       TO_CHAR(re.expense_date, 'YYYY'),
       TO_CHAR(re.expense_date, 'MM')
)
SELECT ds.expense_type_name,
       ds.curr_year,
       ds.curr_month,
       ds.curr_monthly_amount,
       COALESCE(LAG(ds.curr_monthly_amount) OVER (PARTITION BY ds.expense_type_name ORDER BY ds.curr_year, ds.curr_month), 0) AS prev_monthly_amount,
       COALESCE(LEAD(ds.curr_monthly_amount) OVER (PARTITION BY ds.expense_type_name ORDER BY ds.curr_year, ds.curr_month), 0) AS next_monthly_amount
  FROM ds	
order by 
ds.expense_type_name,
ds.curr_year,
ds.curr_month
;
