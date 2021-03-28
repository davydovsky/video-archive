# video-archive

Video archive

This application will help you to maintain your personal video archive.

Based heavily on https://github.com/wemake-services/wemake-django-template


## Prerequisites

You will need:

- `python3.9` (see `pyproject.toml` for full version)
- `mariadb` with version `10.5`
- `rabbitmq` with version `3.8`
- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`


## Development

When developing locally use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- `pycharm 2017+` or `vscode`

## Deployment

You can deploy this app using docker. Pre-build images are located in [docker hub](https://hub.docker.com/r/davydovsky/video-archive/tags?page=1&ordering=last_updated).

There are four docker images:
- [`db-latest`](https://hub.docker.com/layers/davydovsky/video-archive/db-latest/images/sha256-13aff036ecee800febbb0b761806032f801d52e866f7b8ef1d8dc0c2ddd16879?context=explore) which contains MariaDB image
- [`rabbitmq-latest`](https://hub.docker.com/layers/davydovsky/video-archive/rabbitmq-latest/images/sha256-2987cf103a07fe4ca9dbe1922da89307b8e96bdd02fd3e76ed157686f249916e?context=explore) 
which contains preconfigured RabbitMQ image
- [`nginx-latest`](https://hub.docker.com/layers/davydovsky/video-archive/nginx-latest/images/sha256-e09dd85aa4bff1844f3a3f678b5f98d9b492075ae4697075661b9815ca8c950a?context=explore) which contains preconfigured Nginx image
- [`web-latest`](https://hub.docker.com/layers/davydovsky/video-archive/web-latest/images/sha256-894ddc7c7ec6f25be5dfad8712cd15f9104e880123913471e4d4d2c4879574dc?context=explore) contains all application files

### Deploy using Kubernetes 

Application provides a feature of deployment in Kubernetes cluster. Here is an example of deployment in minikube. 
This assumes that you have `minikube` and `kubectl` installed. If not follow this [`official guide`](https://minikube.sigs.k8s.io/docs/start/).
Kubernetes manifests were generated using `kompose` from `./docker/docker-compose.prod.yml`.

First make sure that Ingress addon is enabled.

    $ minikube addons enable ingress
    
Create and fill secrets.

    $ cp ./config/.env_secret.template ./config/.my_env_secret
    $ nano ./config/.my_env_secret
    
    DJANGO_SECRET_KEY=some_secret
    DJANGO_SUPERUSER_PASSWORD=some_superuser_password
    MYSQL_ROOT_PASSWORD=some_db_root_password
    MYSQL_PASSWORD=some_db_password
    RABBITMQ_PASSWORD=some_rabbitmq_password
    
    $ kubectl create secret generic secret--env --from-env-file=./config/.my_env_secret
    
Apply configmap (modify values if needed).

    $ kubectl apply -f ./k8s/config--env-configmap.yaml
    
Apply proxynet, db and rabbitmq.

    $ kubectl apply -f ./k8s/proxynet-networkpolicy.yaml,./k8s/proxynet-networkpolicy.yaml,./k8s/db-deployment.yaml,./k8s/db-service.yaml,./k8s/mdbdata-persistentvolumeclaim.yaml,./k8s/rabbitmq-deployment.yaml,./k8s/rabbitmq-ingress.yaml,./k8s/rabbitmq-service.yaml,./k8s/rabbitmqdata-persistentvolumeclaim.yaml

Set up RabbitMQ user password. Find out RabbitMQ management url.

    $ minikube service --url rabbitmq
    
Go to `http://{url}/#/users/admin` using default `guest:guest` password and change 
admin password to the one you input in secrets. This is inconvenience and will be fixed in the future releases :)

Deploy application and celery workers.

    $ kubectl apply -f ./k8s/celery-workers-deployment.yaml,./k8s/django-locale-persistentvolumeclaim.yaml,./k8s/django-media-persistentvolumeclaim.yaml,./k8s/django-static-persistentvolumeclaim.yaml,./k8s/web-deployment.yaml,./k8s/web-service.yaml

Deploy Nginx.

    $ kubectl apply -f ./k8s/nginx-deployment.yaml,./k8s/nginx-ingress.yaml,./k8s/nginx-service.yaml
    
Make sure that all pods are up and running.

    $ kubectl get pods
    NAME                              READY   STATUS    RESTARTS   AGE
    celery-workers-5b8cd98f46-q2pwc   1/1     Running   0          2m15s
    db-86b58668bd-jf5nr               1/1     Running   0          12m
    nginx-db45f6d9f-mpnh8             1/1     Running   0          11m
    rabbitmq-59ff4d57bb-lmwdf         1/1     Running   0          12m
    web-6cb79699df-dlb74              1/1     Running   1          7m35s

Get app address.
    
    $ minikube service --url nginx
    http://192.168.49.2:31799

## TO DO

- Make proper input file validation
- Do not use tags for different applications
- Make RabbitMQ user configuration automated
- Automating k8s deployment
