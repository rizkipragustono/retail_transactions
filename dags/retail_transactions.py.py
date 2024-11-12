from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.utils.dates import days_ago

# Define default arguments
default_args = {
    'owner': 'rizki',
    'start_date': days_ago(1),
    'retries': 0,
}

# Define ETL functions
def extract_from_postgres(ti, **kwargs):
    pg_hook = PostgresHook(postgres_conn_id="postgres")

    sql_query = "SELECT * FROM retail_transactions ;"
    connection = pg_hook.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql_query)
    data = cursor.fetchall()
    print('data: ', data)
    cursor.close()
    ti.xcom_push(key='data', value=data)

def transform_data(ti, **kwargs):
    extracted_data = ti.xcom_pull(task_ids='extract_from_postgres', key='data')
    transformed_data = [] 
    for row in extracted_data:
        transformed_row = (
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5], 
            row[6], 
            row[7]
        )
        transformed_data.append(transformed_row)

    print('transformed data: ', transformed_data)
    ti.xcom_push(key='transformed_data', value=transformed_data)

def load_into_snowflake(ti, **kwargs):
    transformed_data = ti.xcom_pull(task_ids='transform_data', key='transformed_data')
    if transformed_data:
        snowflake_hook = SnowflakeHook(snowflake_conn_id="snowflake")
        # Create SQL insert statement
        insert_query = """INSERT INTO RETAIL_TRANSACTIONS (id, customer_id, last_status, 
        pos_origin, pos_destination, created_at, updated_at, deleted_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        for row in transformed_data:
            snowflake_hook.run(insert_query, parameters=row)

# Define DAG
with DAG(
    "postgres_to_snowflake_etl",
    default_args=default_args,
    description="ETL DAG to move data from PostgreSQL to Snowflake",
    schedule_interval="@hourly",
) as dag:

    # Task 1: Extract data from PostgreSQL
    extract_task = PythonOperator(
        task_id="extract_from_postgres",
        python_callable=extract_from_postgres,
        provide_context=True,
    )

    # Task 2: Transform the data
    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        provide_context=True,
    )

    # Task 3: Load transformed data into Snowflake
    load_task = PythonOperator(
        task_id="load_into_snowflake",
        python_callable=load_into_snowflake,
        provide_context=True,
    )

    # Define task dependencies
    extract_task >> transform_task >> load_task
