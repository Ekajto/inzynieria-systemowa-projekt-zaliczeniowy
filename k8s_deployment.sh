#!/bin/bash
kubectl create namespace inz-sys-ekajto
kubectl apply -R --namespace=inz-sys-ekajto -f k8s/config
kubectl apply -R --namespace=inz-sys-ekajto -f k8s/db
kubectl apply -R --namespace=inz-sys-ekajto -f k8s/backend
kubectl apply -R --namespace=inz-sys-ekajto -f k8s/frontend