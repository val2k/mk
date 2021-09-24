
# Mk

## Description

Given the problematic, I opted for an Airflow solution which might appear excessive for the use case but which could be the basis of a complete workflow orchestration.

The solution is only intented for local testing and would seem less odd (mix between docker-compose & minikube/helm) for production.

A mount point is set between the mk/dags folder and the Minikube node.

For a production deployment, I would have used Terraform to deploy the Kubernetes cluster and the differents services.

The DAGS would have been synchronized with a GIT repository (gitSync) and the Docker images stored on a (private) repository.

The *Grafana* **PostgreSQL** datasource has been automatically configured and it could be the same for dashboards.

The DAG is scheduled to run automatically each month (first day of the month at 1h AM).

##  Requirements

    - Minikube - Tested with:
        minikube version: v1.21.0
        commit: 76d74191d82c47883dc7e1319ef7cebd3e00ee11
    - Helm - Tested with:
        Version:"v3.6.1", GitCommit:"61d8e8c4a6f95540c15c6a65f36a6dd0a45e7a2f"
    - Docker - Tested with:
        Docker version 20.10.7, build f0df350




## How To ?

### Start the stack

```
    make start
```

`make start` will start the minikube server with the DAGs mount point and install Airflow via Helm. The docker-compose stack will then be started.

Once the stack is up, `make forward_port` will make the AiflowUI available at `localhost:8000`.

### Stop the stack

`eval $(minikube docker-env)`
```
    make stop
```

`make stop` will stop the docker-compose stack, delete Airflow from minikube then delete the minikube cluster.

### Build the ingestor Docker image

```
    make build_ingestor_image
```

This command will synchronize the local / minikube Docker registry. The built image will thus be available from the KubernetesPodOperator.



*Note:* Basically, the process is to have two terminals, one to start the stack, and one to build the image run by the *KubernetesPodOperator*.

### Start the DAG for a specific date/month:
```
    { "year_month": "2021/04" }
```

## Endpoints

    - localhost:8000: Airflow WebUI (The port needs to be forwarded !)
    - localhost:3000: Grafana
        - Note: The PostgreSQL datasource is already defined.

