import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

def process_all_files():
    """Собираем все файлы из /data и записываем их в historical.txt"""
    data_dir = '/home/alex/airflow/data'
    output_file = '/home/alex/airflow/documents/historical.txt'
    
    # Получаем список всех файлов в /data
    all_files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]
    
    # Записываем в файл
    with open(output_file, 'w') as f:
        for file_name in all_files:
            f.write(f"{file_name}\n")
    
    print(f"Записано {len(all_files)} файлов в {output_file}")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='full_load_dag',
    start_date = datetime(2025, 1, 1),
    description='Полная загрузка всех данных',
    schedule=None, 
    catchup=False,
    tags=['full_load'],
) as dag:

    process_all = PythonOperator(
        task_id='process_all_json',
        python_callable=process_all_files,
    )
