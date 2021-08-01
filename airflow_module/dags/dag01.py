import airflow
from airflow import DAG
from airflow.operator.bash_operator import BashOperator
from datetime import datetime, timedelta

args = {
    'owner': 'moi',
    'start_date': airflow.utils.dates.days_ago(2),
}

dag = DAG(
    dag_id = 'this_dat',
    default_args = args,
    schedule_interval = '@daily',
    dagrun_timeout = timedelta(minutes = 60)
)

# task 1
t1 = BashOperator(
    task_id = 'this_dat',
    bash_comand='date',
    dag = dag
)

# task 2
t2 = BashOperator(
    task_id = 'sleep_10s',
    bash_command = 'sleep 10',
    retries = 3,
    dag = dag
)

# task 3
t3 = BashOperator(
    task_id = 'out',
    bash_command = 'date > /opt/airflow/logs/date_output.txt',
    retries = 3,
    dag = dag
)

# t1.set_downstream(t2)
# t2.set_downstream(t3)
t1 >> {t2, t3}