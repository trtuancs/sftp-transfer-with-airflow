from datetime import datetime, timedelta
from airflow import DAG
from configs.ftps import FTPSource, FTPTarget
from libs.ftp import integrate_ftp_server
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 14),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sftp_transfer_dag',
    default_args=default_args,
    description='Transfer files from source SFTP server to target SFTP server',
    schedule_interval=None,
)

integrate_ftp_server_files = PythonOperator(
    python_callable=integrate_ftp_server,
    op_kwargs={
        'source': FTPSource,
        'target': FTPTarget,
    },
    task_id='integrate_ftp_server_files',
    dag=dag
)

integrate_ftp_server_files
