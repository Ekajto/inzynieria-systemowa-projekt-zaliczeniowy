# TODO App

Simple todo application written in python(backend) and vuejs(frontend) with postgres database that serve the purpose of setting up frontend+backend+database application through docker-compose and k8s.

Docker images are available here https://hub.docker.com/u/ekajto

## docker compose

To run

```bash
docker-compose up -d
```

Navigate to http://localhost:80

To stop

```bash
docker-compose down
```

## k8s using minikube

To run minikube first

```bash
minikube start
```

Open tunneling in seperate window

```bash
minikube tunnel
```

To create stack in `inz-sys-ekajto` namespace

```bash
bash k8s_deployment.sh
```

To get frontend url

```bash
minikube service todo-app-front-service -n inz-sys-ekajto --url
```

Follow provided url
