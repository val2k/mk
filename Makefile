CURRENT_DIR := $(shell pwd)

build_image:
	@eval $$(minikube docker-env) ;\
	docker build -t ingestor:latest ./mk/ingestor

forward_port:
	kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow --kubeconfig ~/.kube/config

get_pods:
	kubectl get pods --kubeconfig ~/.kube/config --namespace airflow

start:
	minikube start --mount=true --mount-string=$(CURRENT_DIR)/mk/dags/:/mnt/airflow/dags_mk/
	./airflow/install_airflow_on_minikube.sh
	docker-compose up -d

stop:
	docker-compose down
	helm delete airflow --kubeconfig ~/.kube/config --namespace airflow || true
	minikube delete

