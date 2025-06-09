# from airflow import DAG
# from airflow.operators.python import PythonOperator
# from datetime import datetime
# import json

# def transform_json():
#     # Путь к исходному JSON
#     input_path = "/home/alex/airflow/data/pets.json"
#     output_path = "/home/alex/airflow/data/linear_pets.json"
    
#     # Чтение JSON
#     with open(input_path, "r") as f:
#         data = json.load(f)
    
#     # Извлекаем список pets и сохраняем как новый JSON
#     linear_data = data["pets"]
    
#     # Запись результата
#     with open(output_path, "w") as f:
#         json.dump(linear_data, f, indent=2)
    
#     print(f"Результат сохранён в {output_path}")

# # Определяем DAG
# dag = DAG(
#     "json_to_linear",
#     start_date=datetime(2025, 6, 9),
#     schedule=None,  # Запуск только вручную
#     catchup=False,
# )

# # Задача для преобразования
# transform_task = PythonOperator(
#     task_id="transform_json",
#     python_callable=transform_json,
#     dag=dag,
# )

from airflow.decorators import dag, task
from datetime import datetime
import json
from pathlib import Path

# Пути к файлам (используем Path для кроссплатформенности)
INPUT_JSON = Path("/home/alex/airflow/data/pets.json")  # Замените 'alex' на ваш username в WSL
OUTPUT_JSON = Path("/home/alex/airflow/data/linear_pets.json")

@dag(
    dag_id="json_to_linear",
    schedule=None,  # Запуск только вручную
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["json", "transform"],
)
def transform_json_to_linear():
    @task
    def load_and_transform():
        """Загружает JSON и преобразует его в линейную структуру."""
        try:
            # Чтение файла
            data = json.loads(INPUT_JSON.read_text())
            linear_data = data["pets"]
            
            # Запись результата
            OUTPUT_JSON.parent.mkdir(exist_ok=True, parents=True)  # Создать папку, если её нет
            OUTPUT_JSON.write_text(json.dumps(linear_data, indent=2))
            
            return f"Файл успешно сохранён: {OUTPUT_JSON}"
        except Exception as e:
            raise RuntimeError(f"Ошибка: {e}")

    # Запуск задачи
    load_and_transform()

# Создаем DAG
dag = transform_json_to_linear()