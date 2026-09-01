# GitOps-based Kubernetes deployment

## Introduction

This project demonstrates a GitOps-based Kubernetes deployment workflow using GitHub Actions and Argo CD. Each push to the main branch triggers a CI pipeline that builds and publishes a container image to GitHub Container Registry (GHCR) and updates the Kubernetes deployment manifest. Argo CD monitors the Git repository and automatically synchronizes the desired state with a local Kubernetes cluster running on kind.

The project intentionally separates CI from CD: GitHub Actions builds and publishes the application artifact, while Argo CD is responsible for deploying it to Kubernetes.

## Architecture diagram

![GitOps CI/CD Architecture](<Diagram.png>)

## How it works

The deployment flow is:

1. A developer pushes changes to the `main` branch.
2. GitHub Actions is triggered.
3. GitHub Actions builds the application container image.
4. The image is pushed to GitHub Container Registry (GHCR).
5. The Kubernetes manifest is updated with the new image version.
6. The manifest change is committed and pushed to Git.
7. Argo CD detects the change in the Git repository.
8. Argo CD automatically synchronizes the desired state with the Kubernetes cluster.
9. Kubernetes deploys the updated application.

## Technology choices

### Github Actions
GitHub Actions was selected because the source code and CI workflow can be managed within the same GitHub repository.

In this project, GitHub Actions is responsible for:
- Building the Docker image
- Publishing the image to GHCR
- Updating the Kubernetes manifest

### ArgoCD vs FluxCD

Argo CD was selected to implement the CD/GitOps layer because of its web UI that provides clear visibility into the application health, synchronization status, configuration differences, and deployment history.

Argo CD was preferred over Flux for this project primarily because its UI makes GitOps synchronization and application state particularly easy to inspect.

### Kind vs Minikube

Kind provides a lightweight and reproducible Kubernetes cluster suitable for simple local experimentation and CI-oriented workflows. Minikube was considered as an alternative, but kind was preferred for this project's lightweight and Kubernetes-focused setup.

### Polling vs webhook-triggered synchronization

Polling was retained to keep the local setup simple and avoid exposing the local Argo CD instance through a public webhook endpoint.
For a production deployment, a Git webhook could be introduced to reduce the delay between a Git change and Argo CD reconciliation.

## What this demonstrates

### Gitbased deployment (GitOps)

Kubernetes manifests stored in Git provide a versioned source of truth for the desired cluster state.

### Separation CI/CD

Deployment responsibility is intentionally separated from the CI pipeline.
GitHub Actions builds and publishes the application artifact but does not directly access the Kubernetes API.

### Automated Container Builds

Every push to the `main` branch triggers the GitHub Actions workflow, which builds the application container image and publishes it to GHCR.

### Automated Kubernetes Synchronization

Argo CD continuously monitors the Git repository and automatically synchronizes Kubernetes resources when the desired state changes.

## Repository structure

<pre>
  gitops-argocd-demo
  ├── .github/
  │    └── workflows/
  │        └── docker-build.yml
  ├── app/
  │   ├── app.py
  │   ├── Dockerfile
  │   └── requirements.txt
  ├── manifests/
  │   ├── deployment.yaml
  │   └── service.yaml
  ├── Diagram
  └── README.md
</pre>

## Prerequisites

This project was developed on **Windows using WSL2/Ubuntu**.

The instructions below assume that the following tools are already installed and configured:

- Docker
- kubectl
- Git
- kind

PS: WSL2/Ubuntu is an environment requirement rather than part of the project's infrastructure. The deployment itself relies on Docker, kind, kubectl, GitHub Actions, GHCR, and Argo CD.

## Running it locally

Before deploying to Kubernetes, the container can be tested independently using Docker.

1. Build the image
Command
```bash docker build -t gitops-demo-app:v1 .```

2. Run the container
Command:
```bash docker run -d -p 5000:5000 --name demo-test gitops-demo-app:v1```

3. Check the user:
Command:
```bash docker exec demo-test whoami```
Output:
```app```
4. Check the application responsiveness
Command:
```bash curl localhost:5000```
Output:
GitOps demo app is running
5. Check the release version
Command:
```bash curl localhost:5000/version```
Output:
```v1```

See the [Dockerfile](./app/Dockerfile) for the container configuration.


## Known limitations

This project intentionally runs on a local Kubernetes cluster and is designed as a GitOps learning/portfolio project rather than a production deployment.

Current limitations include:

- Local Kubernetes cluster
- Single application
- No external ingress/load balancer
- No secrets management solution
- No production-grade observability stack
- Git polling rather than an externally accessible webhook

## Troubleshooting Notes

**Docker permission in WSL**

During the initial setup, Docker and kind commands required ```sudo```. 

The issue? The current Linux user was not part of the ```docker``` group.

To fix it, there are 2 solutions :
1. Write ```sudo``` before every docker-touching 
2. Add the user docker to the group

The second approach is more practical.
Add the current user to the Docker group:
```bash sudo usermod -aG docker $USER```
After logging out and back in, or restarting the WSL session, verify the user's groups:
```bash groups```

## Future Improvements

- Replace local Kubernetes with a managed Kubernetes cluster.
- Add GitHub webhook integration to reduce Git reconciliation latency.
- Introduce Helm or Kustomize for environment-specific configuration.
- Add Prometheus/Grafana for monitoring and observability.
- Add automated security scanning for container images.

GitHub Actions | Kubernetes | Argo CD | Docker | GitOps

## Tech Stack

- **Kubernetes**:
  - Excellent control of the resources: ```resources.requests ```/```resources.requests ```allows to get a precise control over the resouces to prevent the container to go wild and accaparate all the resources for itself or to starve and not get enough.

  