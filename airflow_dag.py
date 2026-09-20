from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Default arguments for the DAG
default_args = {
    'owner': 'aiops_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define Task Functions
def collect_metrics(**context):
    metrics = {
        'CPU': 87,
        'Memory': 65,
        'Response_Time': '420ms'
    }
    print(f"Collected Metrics: CPU={metrics['CPU']}%, Memory={metrics['Memory']}%, Response Time={metrics['Response_Time']}")
    # Pass metrics to downstream tasks via XCom
    context['ti'].xcom_push(key='server_metrics', value=metrics)

def process_metrics(**context):
    ti = context['ti']
    metrics = ti.xcom_pull(key='server_metrics', task_ids='collect_metrics')
    print(f"Processing metrics: {metrics}")

def detect_anomaly(**context):
    ti = context['ti']
    metrics = ti.xcom_pull(key='server_metrics', task_ids='collect_metrics')
    cpu = metrics.get('CPU', 0)
    
    if cpu > 80:
        print("Anomaly detected: High CPU usage")
    else:
        print("No anomaly detected")

def generate_report():
    print("===== AIOps Report =====")
    print("Metrics collected successfully")
    print("Metrics processed successfully")
    print("Anomaly detection completed")
    print("================ physics=")

# Define the DAG
with DAG(
    'aiops_workflow_dag',
    default_args=default_args,
    description='A basic AIOps workflow DAG for metrics and anomaly detection',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Task 1: Collect Metrics
    task_collect = PythonOperator(
        task_id='collect_metrics',
        python_callable=collect_metrics,
        provide_context=True,
    )

    # Task 2: Process Metrics
    task_process = PythonOperator(
        task_id='process_metrics',
        python_callable=process_metrics,
        provide_context=True,
    )

    # Task 3: Detect Anomaly
    task_detect = PythonOperator(
        task_id='detect_anomaly',
        python_callable=detect_anomaly,
        provide_context=True,
    )

    # Task 4: Generate Report
    task_report = PythonOperator(
        task_id='generate_report',
        python_callable=generate_report,
    )

    # Define DAG Dependencies
    task_collect >> task_process >> task_detect >> task_report