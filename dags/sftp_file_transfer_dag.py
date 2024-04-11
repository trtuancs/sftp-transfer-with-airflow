from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 4, 11),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    'hello_world_dag',
    default_args=default_args,
    description='A simple DAG that prints Hello, World!',
    schedule_interval=None,  # Set to None to disable automatic scheduling
)

# Define the Python function to print "Hello, World!"
def print_hello():
    print("Hello, World!")

# Define the task using the PythonOperator
print_hello_task = PythonOperator(
    task_id='print_hello_task',
    python_callable=print_hello,
    dag=dag,
)

# Set task dependencies
print_hello_task

