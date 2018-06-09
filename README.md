# simple-project-on-k8s

## minikube

```console
$ minikube start --cpus=4 --memory=8000
$ eval $(minikube docker-env)

$ export PROJECT_ID=simple-project-198818

$ minikube ip
192.168.99.100

$ minikube dashboard
http://192.168.99.100:30000/
```

### simple-api

```console
$ docker build --rm -t asia.gcr.io/${PROJECT_ID}/simple-api:v1 simple-api/

$ kubectl apply -f infrastructure/simple-api/ -R

$ kubectl get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP                      21h
simple-api   NodePort    10.104.48.197   <none>        80:30723/TCP,443:32082/TCP   1m

$ minikube service simple-api

$ curl http://192.168.99.100:30723/
You hit "simple-api-778c45c897-fl5sn" at 2018-03-11T11:57:35.319047+00:00

$ kubectl delete -f infrastructure/simple-api/ -R
```

### simple-frontend

```console
$ docker build --rm -t asia.gcr.io/${PROJECT_ID}/simple-frontend:v1 simple-frontend/

$ kubectl apply -f infrastructure/simple-frontend/ -R
```

### Ingress

```console
$ vim /private/etc/hosts
192.168.99.100  simple-project.com
192.168.99.100  api.simple-project.com

$ kubectl apply -f infrastructure/ingress.yaml

$ kubectl describe ing simple-project
```

## Google Kubernetes Engine

```console
$ gcloud config set compute/region asia-east1
$ gcloud config set compute/zone asia-east1-a

$ gcloud container get-server-config

$ gcloud container clusters create simple-project \
--cluster-version=1.9.4-gke.1 \
--node-version=1.9.4-gke.1 \
--num-nodes=3 \
--machine-type=g1-small \
--enable-legacy-authorization

$ gcloud config set project simple-project-198818 && \
export PROJECT_ID="$(gcloud config get-value project -q)"

$ gcloud container clusters get-credentials simple-project

$ gcloud auth configure-docker

$ export PROJECT_ID="$(gcloud config get-value project -q)" && \
docker build --rm -t asia.gcr.io/${PROJECT_ID}/simple-api:v1 simple-api/ && \
docker push asia.gcr.io/${PROJECT_ID}/simple-api:v1 && \
kubectl apply -f infrastructure/simple-api/ -R && \
docker build --rm -t asia.gcr.io/${PROJECT_ID}/simple-frontend:v1 simple-frontend/ && \
docker push asia.gcr.io/${PROJECT_ID}/simple-frontend:v1 && \
kubectl apply -f infrastructure/simple-frontend/ -R

$ kubectl apply -f infrastructure/ingress.yaml

$ kubectl describe ing simple-project

# add A records to your domains which point to the "Address" of the Ingress

$ kubectl apply -f infrastructure/helm/ -R && \
helm init --service-account tiller

$ helm install \
--name cert-manager \
stable/cert-manager

$ helm ls --all cert-manager

$ kubectl logs deployment/cert-manager-cert-manager cert-manager -f

$ kubectl apply -f infrastructure/cert-manager/ -R

$ kubectl get certificates
$ kubectl describe certificate kittenphile-com

$ kubectl apply -f infrastructure/kube-lego -R
$ kubectl replace --force -f infrastructure/kube-lego -R

$ kubectl describe ing simple-project

$ gcloud container clusters delete simple-project
```
