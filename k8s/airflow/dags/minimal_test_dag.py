# minimal_test_dag.py
from airflow import DAG
from airflow.operators.empty import EmptyOperator # A simple operator that does nothing
from datetime import datetime

with DAG(
    dag_id='minimal_test_dag',
    start_date=datetime(2023, 1, 1),
    schedule=None, # Set schedule to None for manual trigger only
    catchup=False,
    tags=['minimal'],
) as dag:
    start_task = EmptyOperator(task_id='start_minimal_task')