from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_data():
    # Загрузка данных из CSV
    df = pd.read_csv('/home/alex/airflow/data/IOT-temp.csv')  # Укажите правильный путь к файлу
    return df

def filter_in_data(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='load_data')
    
    # Фильтрация только входящих данных (in)
    filtered_df = df[df['out/in'] == 'In'].copy()
    return filtered_df

def convert_date_format(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='filter_in_data')
    
    # Преобразование формата даты
    df['noted_date'] = pd.to_datetime(df['noted_date'], format='%d-%m-%Y %H:%M').dt.date
    return df

def clean_temperature(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='convert_date_format')
    
    # Очистка температуры по 5-му и 95-му процентилю
    lower_bound = df['temp'].quantile(0.05)
    upper_bound = df['temp'].quantile(0.95)
    
    cleaned_df = df[(df['temp'] >= lower_bound) & (df['temp'] <= upper_bound)].copy()
    return cleaned_df

def find_extreme_days(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(task_ids='clean_temperature')
    
    # Группировка по дате и вычисление средней температуры
    daily_temp = df.groupby('noted_date')['temp'].mean().reset_index()
    
    # 5 самых жарких дней
    hottest_days = daily_temp.nlargest(5, 'temp')
    
    # 5 самых холодных дней
    coldest_days = daily_temp.nsmallest(5, 'temp')
    
    # Сохранение результатов
    hottest_days.to_csv('/home/alex/airflow/data/hottest_days.csv', index=False)  # Укажите путь для сохранения
    coldest_days.to_csv('/home/alex/airflow/data/coldest_days.csv', index=False)  # Укажите путь для сохранения
    
    return {
        'hottest_days': hottest_days.to_dict(),
        'coldest_days': coldest_days.to_dict()
    }

with DAG(
    dag_id = 'temperature_processing',
    description='DAG для обработки данных о температуре',
    start_date = datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    filter_in_data_task = PythonOperator(
        task_id='filter_in_data',
        python_callable=filter_in_data,
    )

    convert_date_format_task = PythonOperator(
        task_id='convert_date_format',
        python_callable=convert_date_format,
    )

    clean_temperature_task = PythonOperator(
        task_id='clean_temperature',
        python_callable=clean_temperature,
    )

    find_extreme_days_task = PythonOperator(
        task_id='find_extreme_days',
        python_callable=find_extreme_days,
    )

    load_data_task >> filter_in_data_task >> convert_date_format_task >> clean_temperature_task >> find_extreme_days_task