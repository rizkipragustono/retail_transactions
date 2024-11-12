from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime

# Define the DAG
dag = DAG(
    'test_postgres_connection',  # DAG name
    description='A simple DAG to test PostgreSQL connection',
    schedule_interval=None,  # This DAG will not run on a schedule, only on trigger
    start_date=datetime(2024, 11, 12),  # Use the current date or modify it
    catchup=False,  # Do not backfill past DAG runs
)

# Task to test the PostgreSQL connection by running a simple query
test_postgres_connection = PostgresOperator(
    task_id='test_connection',  # Task ID
    postgres_conn_id='postgres',  # Use the connection ID defined in Airflow UI
    sql="SELECT * from retail_transactions;",  # Simple SQL query to test connection
    dag=dag,
)

# Set the task sequence (though only one task in this case)
test_postgres_connection
