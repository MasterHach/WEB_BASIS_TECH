import os
import time
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def get_recent_files(days=3):
    """Получаем файлы, измененные за последние N дней"""
    data_dir = '/home/alex/airflow/data'
    now = time.time()
    time_threshold = now - (days * 86400)  # days в секундах
    
    recent_files = []
    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            if mod_time >= time_threshold:
                recent_files.append(file_name)
    
    return recent_files

def process_recent_files(**context):
    """Собираем недавние файлы и записываем их в incremental.txt"""
    days = context['params'].get('days', 3)
    output_file = '/home/alex/airflow/documents/incremental.txt'
    
    recent_files = get_recent_files(days)
    
    # Записываем в файл
    with open(output_file, 'w') as f:
        for file_name in recent_files:
            f.write(f"{file_name}\n")
    
    print(f"Записано {len(recent_files)} недавних файлов в {output_file}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='incremental_load_dag',
    description='Инкрементальная загрузка (только изменения)',
    start_date = datetime(2025, 1, 1),
    schedule=None,  # Ежедневно в полночь
    catchup=False,
    tags=['incremental'],
) as dag:

    save_recent_files = PythonOperator(
        task_id='save_recent_files',
        python_callable=process_recent_files,
        params={'days': 3},
    )