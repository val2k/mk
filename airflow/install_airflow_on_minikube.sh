#!/usr/bin/bash

export AIRFLOW_DIR=$(dirname $(realpath $0))
export AIRFLOW_NAME="airflow"
export AIRFLOW_NAMESPACE="airflow"

kubectl create namespace $AIRFLOW_NAMESPACE \
	--kubeconfig ~/.kube/config

helm repo add apache-airflow https://airflow.apache.org
helm install $AIRFLOW_NAME apache-airflow/airflow \
    --values $AIRFLOW_DIR/values.yml \
    --set logs.persistence.enabled=true \
    --namespace $AIRFLOW_NAMESPACE \
    --kubeconfig ~/.kube/config
