from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime

# Define the DAG
dag = DAG(
    'test_snowflake_connection',  # DAG name
    description='A simple DAG to test snowflake connection',
    schedule_interval=None,  # This DAG will not run on a schedule, only on trigger
    start_date=datetime(2024, 11, 12),  # Use the current date or modify it
    catchup=False,  # Do not backfill past DAG runs
)

# Task to test the PostgreSQL connection by running a simple query
test_snowflake_connection = SnowflakeOperator(
    task_id='test_connection',  # Task ID
    snowflake_conn_id='snowflake',  # Use the connection ID defined in Airflow UI
    sql="SELECT 1;",  # Simple SQL query to test connection
    dag=dag,
)

# Set the task sequence (though only one task in this case)
test_snowflake_connection