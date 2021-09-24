import datetime

from airflow import models
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

from kubernetes.client import models as k8s

DEFAULT_ARGS = {
    'email': ['kinyock.va@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 0,
    'retry_delay': datetime.timedelta(minutes=5)
}

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)
JINJA_DATE_TERNARY = "{{ dag_run.conf['year_month'] if 'year_month' in dag_run.conf else '' }}"
SCHEDULE_INTERVAL = '0 1 1 * *'

with models.DAG(
        dag_id='events_ingestor_dag',
        default_args=DEFAULT_ARGS,
        schedule_interval=SCHEDULE_INTERVAL,
        start_date=YESTERDAY) as dag:

    kubernetes_min_pod = KubernetesPodOperator(
        task_id='events_ingestor_task',
        name='events_ingestor_task',
        cmds=['python', 'ingestor.py', "--year-and-month", JINJA_DATE_TERNARY],
        namespace='airflow',
        is_delete_operator_pod=False,
        image='ingestor:latest',
        get_logs=True,
        image_pull_policy='Never',
        executor_config={
            "pod_override": k8s.V1Pod(
                spec=k8s.V1PodSpec(
                    containers=[
                        k8s.V1Container(
                            name="base",
                            volume_mounts=[
                                k8s.V1VolumeMount(
                                    mount_path="/opt/airflow/dags", name="dags-volume"
                                )
                            ],
                        )
                    ],
                    volumes=[
                        k8s.V1Volume(
                            name="dags-volume",
                            host_path=k8s.V1HostPathVolumeSource(path="/mnt/airflow/dags_mk"),
                        )
                    ],
                )
            ),
        },
    )
