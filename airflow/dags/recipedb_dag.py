import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Add the parent directory to the sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, parent_dir)

from etls.extract.crawl_bachhoaxanh import bhx_spider
# from etls.crawl_cookpad import crawl_cookpad
from etls.extract.api_spoonacular import spoonacularExtractAPI
from utils import load_to_mongodb, load_to_postgresql
# from etls.transforms import transform_bachhoaxanh
# from etls.transforms.transform_cookpad import transform_cookpad
# from etls.transforms import transform_spoonacular

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
}
def example_function():
    print('Hello World')

dag = DAG('recipedb_dag', default_args=default_args, schedule_interval='@daily')

example_task = PythonOperator(
    task_id='example',
    python_callable=example_function,
    dag=dag
)

crawl_bachhoaxanh_task = PythonOperator(
    task_id='bhx_spider',
    python_callable=bhx_spider,
    dag=dag
)

# crawl_cookpad_task = PythonOperator(
#     task_id='crawl_cookpad',
#     python_callable=crawl_cookpad,
#     dag=dag
# )

# api_spoonacular_task = PythonOperator(
#     task_id='1',
#     python_callable=spoonacularExtractAPI,
#     dag=dag
# )

# load_to_mongodb_task = PythonOperator(
#     task_id='2',
#     python_callable=load_to_mongodb,
#     dag=dag
# )

# transform_bachhoaxanh_task = PythonOperator(
#     task_id='transform_bachhoaxanh',
#     python_callable=transform_bachhoaxanh,
#     dag=dag
# )

# transform_cookpad_task = PythonOperator(
#     task_id='transform_cookpad',
#     python_callable=transform_cookpad,
#     dag=dag
# )

# transform_spoonacular_task = PythonOperator(
#     task_id='3',
#     python_callable=transform_spoonacular,
#     dag=dag
# )

# load_to_postgresql_task = PythonOperator(
#     task_id='load_to_postgresql',
#     python_callable=load_to_postgresql,
#     dag=dag
# )

# Define task dependencies
# crawl_bachhoaxanh_task >> load_to_mongodb_task
# crawl_cookpad_task >> save_raw_to_mongodb_task
# api_spoonacular_task >> load_to_mongodb_task

# save_raw_to_mongodb_task >> transform_bachhoaxanh_task
# save_raw_to_mongodb_task >> transform_cookpad_task
# save_raw_to_mongodb_task >> transform_spoonacular_task

# transform_bachhoaxanh_task >> load_to_postgresql_task
# # transform_cookpad_task >> load_to_postgresql_task
# transform_spoonacular_task >> load_to_postgresql_task