from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'aiops_engineer',
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

def collect_metrics(**kwargs):
    metrics = {'CPU': 87, 'Memory': 65, 'Response Time': '420ms'}
    print(f"Collected Metrics: CPU = {metrics['CPU']}%, Memory = {metrics['Memory']}%, Response Time = {metrics['Response Time']}")
    return metrics

def process_metrics(**kwargs):
    ti = kwargs['ti']
    metrics = ti.xcom_pull(task_ids='collect_metrics')
    print(f"Processing collected metrics: {metrics}")
    return metrics

def detect_anomaly(**kwargs):
    ti = kwargs['ti']
    metrics = ti.xcom_pull(task_ids='process_metrics')
    cpu = metrics.get('CPU', 0) if metrics else 0
    
    if cpu > 80:
        print("Anomaly detected: High CPU usage")
    else:
        print("No anomaly detected")

def generate_report(**kwargs):
    print("===== AIOps Report =====")
    print("Metrics collected successfully")
    print("Metrics processed successfully")
    print("Anomaly detection completed")
    print("========================")

with DAG(
    'aiops_workflow_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    t1 = PythonOperator(task_id='collect_metrics', python_callable=collect_metrics)
    t2 = PythonOperator(task_id='process_metrics', python_callable=process_metrics)
    t3 = PythonOperator(task_id='detect_anomaly', python_callable=detect_anomaly)
    t4 = PythonOperator(task_id='generate_report', python_callable=generate_report)

    t1 >> t2 >> t3 >> t4