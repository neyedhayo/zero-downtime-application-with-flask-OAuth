# Guide-to-Setup: Twitter OAuth in Flask Application with Zero-Downtime Upgrade deployment implementation

## Introduction

This guide covers the steps to set up a Flask application with Twitter OAuth, deploy it to a Kubernetes cluster with a zero-downtime upgrade strategy, implement and verify a new version of the application to ensure zero downtime.

## Resources (Docs)

- [K8s Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- 

## Tools

* Flask
* Twitter(X) OAuth
* Kubernetes
* Docker
* Git
* Gardener (AWS platform)

## Prerequisites

* Python should already be installed in your machine
* Docker installed on your local machine.
* Access to a Docker registry (e.g., Docker Hub).
* Kubernetes cluster (Gardener or any other provider) and kubectl installed.
* Twitter Developer Account for OAuth credentials.

## 1. Setup Flask Application with Twitter OAuth

1. Make sure you have the `app.py` file is created in the parent directory
2. Ensure you have the `requirement.txt` file and executed in the terminal

   ```txt
    Flask==2.0.1
    tweepy==4.0.0
    python-dotenv==0.19.0
   ```

3. The `Dockerfile` should also be in the same directory as well
4. Most importantly create `.env` file where your client credentials will be saved in.

   ```env
    TWITTER_CONSUMER_KEY=...
    TWITTER_CONSUMER_SECRET=...
    TWITTER_ACCESS_TOKEN=...
    TWITTER_ACCESS_TOKEN_SECRET=...
   ```

**WARNING:** The `env` should be kept private and not open to public, one way to ensure that is by ignoring it in a `.gitignore` file as used in this workflow or manually setting the OAuth tokens as a enviroment variable via terminal **(NOT used!)**

5. You can run the application manually if you want, simply by;

   ```python
   python3 app.py
   ```

<br>

> Although here in our case, we're integrating the application to a K8s cluster on Gardener AWS platform

## 2. Deploying to Kubernetes with Zero-Downtime Upgrades

1. Build and the push Docker image

   ```bash
   docker build -t your-name/twitter:v1 .
   docker push your-name/twitter:v1
   ```

2. Create the Kubernetes deployment manifest file - `deployment.yaml`; <br>
   Creating the file, the important steps to integrate the **"zero-downtime upgrades"** will be;

    * The "strategy rolling-update" field in the specifications ;

        ```yaml
        spec:
            replicas: 3
            selector:
                matchLabels:
                app: app
            strategy: # field to enable the rolling update for downtime upgrade
                type: RollingUpdate 
                rollingUpdate:
                    maxUnavailable: 1
                    maxSurge: 1
        ```

    * The constraints topology for the server zone

        ```yaml
        topologySpreadConstraints:
        - maxSkew: 1
            topologyKey: "topology.kubernetes.io/zone"
            whenUnsatisfiable: DoNotSchedule
            labelSelector:
            matchLabels:
                app: app
        ```

3. Ensure you have your `service.yaml` file which contains the LoadBalancer specifications in the parent directory

4. Create Kubernetes Secrets for Twitter Credentials

    ```sh
    kubectl create secret generic twitter-credentials \
        --from-literal=consumer_key=inputkey \
        --from-literal=consumer_secret=inputkey \
        --from-literal=access_token=inputkey \
        --from-literal=access_token_secret=inputkey
    ```

    **NOTE:** In this step, if your output is returning an already existing client credentials, you'll have to delete it and re-run the above shell script. To delete the old saved credentials if necessary;

    ```sh
    kubectl delete secret twitter-credentials
    ```

5. Deploy to the Kubernetes cluster

    ```sh
    kubectl apply -f deployment.yaml
    kubectl apply -f service.yaml
    ```

6. Monitor the Deployment

    ```sh
    kubectl rollout status deployment/app
    ```

7. Running the application with the external IP of the loadbalancer

    ```sh
    kubectl get services
    ```

    **Get the external IP url of the running application and paste it on your browser**.

## 3. Implementing and Verifying Zero-Downtime Upgrade

1. Modify your application code for a new version i.e your `app.py` and save it!

2. Build a new Docker image

    ```sh
        docker build -t your-username/twitter:v2 .
    ```

3. Push the New Docker Image

    ```sh
        docker push your-username/twitter:v2
    ```

4. Update the Deployment Manifest
    <br>

    From the `deployment.yaml` file, update the image field in the containers section to the new app version, using the image tag **(`v2`)** e.g.

    ```yaml
        containers:
        - name: twitter
            image: your-username/twitter:v2
        ...
    ```

5. Apply the Updated Deployment

    ```sh
        kubectl apply -f deployment.yaml
    ```

6. Verify the Rolling Update
    <br>

    Monitor the rollout status to ensure zero downtime:

    ```sh
        kubectl rollout status deployment/app
    ```

7. Check the Status of Pods

    ```sh
        kubectl get pods
    ```

8. Access the Updated Application
   <br>

   Use the external IP provided by your LoadBalancer service to access the updated application. You can get that with;

    ```sh
        kubectl get services
    ```

## CONCLUSION

With this guide, you will be able to setup a Flask application with Twitter OAuth, deploy it to a Kubernetes cluster with a zero-downtime upgrade strategy, and implement and verify a new version of the application to ensure zero downtime