# Data Validation Script

This folder contains the script and files necessary to run data validation via Cronjob on a Kubernetes namespace.

# Setup Instructions

## 1. Set up Azure

- Ensure Azure CLI in installed on your system, as well as kubectl and helm. These will be required to connect to Azure Container Registry.
```
// Install kubectl
az aks install-cli

// Install helm
az acr helm install-cli
```

- Open a terminal and log in to Azure CLI. You may be redirected to a browser to complete the login process.
```
az login
```
- Create a Container registry on ACR
- Log in to Azure Container Registry CLI using credentials generated for the registry.
```
az acr login --name RegistryName --username RegistryUsername --password RegistryPassword1 --reesource-group ResourceGroupName
```
Ensure that any issues with dependencies mentioned by the CLI messages are resolved.

- Once login is successful, list the repositories in the registry to ensure that access is working properly.
```
az acr repository list --name RegistryName
```
For any issues, you can refer the CLI [docs](https://docs.microsoft.com/en-us/cli/azure/acr?view=azure-cli-latest)

## 2. Build and publish script image to ACR

On Kubernetes, Cronjobs are run by pulling container images for the script from the location provided under the 'image' field the YAML file.
To build the image for our script:

- Ensure that you are logged into to Azure CLI as well as the ACR CLI. Refer to the [previous](#set-up-azure) section for assistance.

- Navigate to the /cronjob folder in this project and open a terminal. Ensure that the folder path directly contains the Dockerfile for the script.

- Build the docker image.
```
docker build -t docker-image-name .
```

- Tag docker image with registry details.
```
docker tag docker-image-name acr-domain/image-repo-name
```

- Push docker image to ACR repo.
```
docker push acr-domain/image-repo-name
```

- The ACR registry should now contain a new repository with the image available.


## 3. Deploy CronJob to Kubernetes

Like with most Kubernetes resources, we will create the cronjob for the script by applying our YAML file in the target namespace.

- Ensure that the following Secrets are available in Kubernetes.
    * ACR credentials secrets
    * CronJob envvars secrets

- Modify the existing ckan-cron-job.yaml file to replace the tagged placeholders with the actual values.
    * ACR credentials secrets name.
    * Image registry location.
    * CronJob envvars secrets name.

- Navigate to `/cronjob` folder and open a terminal where the YAML file is located.

- Login to Azure CLI as mentioned [here](#set-up-azure). Ensure that Kubectl is installed.

- Ensure you have the credentials for accessing your Kubernetes cluster.
```
az aks get-credentials --name KubernetesClusterName --resource-group ResourceGroupName
```

- Set context for Kubectl to connect to your Kubernetes cluster. This is especially required if you manage multiple clusters.
```
kubectl config use-context KubernetesClusterName
```

- Apply CronJob YAML to the required namespace in your cluster.
```
kubectl create -f ./ckan-cron-job.yaml -n ClusterNamespace
```
Now CronJob should be available on the provided Namespace in your Kubernetes Cluster

## Running CronJobs

You can access your Cronjobs just like any other Kubernetes resources via [Lens](https://k8slens.dev/)

- Connect to your Kubernetes cluster in Lens and select `CronJobs` tab from the `Workloads` section of the side menu.

- On clicking the `CronJobs` tab, a side window will open with details regarding the CronJob. There will be a number of buttons on the top right side of the side window.

- While CronJobs are scheduled jobs, they can also be triggered manually by clicking the play button in the side window as mentioned above.

- The jobs will execute as individual pods  where you can check for logs as well. Only 3 pods will be retained at a time for this cronjob, with older pods being terminated as new ones are created.