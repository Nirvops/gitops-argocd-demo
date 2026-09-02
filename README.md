# GitOps-based Kubernetes deployment

## Introduction

This project demonstrates a GitOps-based Kubernetes deployment workflow using GitHub Actions and Argo CD. Each push to the main branch triggers a CI pipeline that builds and publishes a container image to GitHub Container Registry (GHCR). Argo CD monitors the Git repository and synchronizes the desired state with a local Kubernetes cluster running on kind.

The project intentionally separates CI from CD: GitHub Actions builds and publishes the application artifact, while Argo CD is responsible for deploying it to Kubernetes.

## Architecture diagram

![GitOps CI/CD Architecture](<Diagram.png>)

## How it works

The deployment flow is:

1. A developer pushes changes to the `main` branch.
2. GitHub Actions is triggered.
3. GitHub Actions builds the application container image.
4. The image is pushed to GitHub Container Registry (GHCR).
5. The image tag is updated manually in the deployment manifest to reference the new build, then committed.
6. Argo CD detects the change and the deployment is manually synced via the UI
7. Kubernetes deploys the updated application.

## Technology choices

### Github Actions
GitHub Actions was selected because the source code and CI workflow can be managed within the same GitHub repository.

In this project, GitHub Actions is responsible for:
- Building the Docker image
- Publishing the image to GHCR

### ArgoCD vs FluxCD

Argo CD was selected to implement the CD/GitOps layer partly due to prior familiarity, and partly due to its UI that provides clear visibility into the application health, synchronization status, configuration differences, and deployment history.

It makes GitOps synchronization and application state particularly easy to inspect.

### Kind vs Minikube

Kind provides a fast local setup/teardown. In addition, kind's "nodes are just containers" model is simpler to understand and reason about. 

### Polling vs webhook-triggered synchronization

Polling was retained to keep the local setup simple and avoid exposing the local Argo CD instance through a public webhook endpoint. Plus no configuration was required which is simpler.
For a production deployment, a Git webhook could be introduced to reduce the delay between a Git change and Argo CD reconciliation.

## What this demonstrates

### Git-based deployment (GitOps)

Kubernetes manifests stored in Git provide a versioned source of truth for the desired cluster state.

### Separation CI/CD

Deployment responsibility is intentionally separated from the CI pipeline.
GitHub Actions builds and publishes the application artifact but does not directly access the Kubernetes API.

### Automated Container Builds

Every push to the `main` branch triggers the GitHub Actions workflow, which builds the application container image and publishes it to GHCR.


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
  ├── Diagram.png
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
```docker build -t gitops-demo-app:v1 .```

2. Run the container
Command:
```docker run -d -p 5000:5000 --name demo-test gitops-demo-app:v1```

3. Check the user:
Command:
```docker exec demo-test whoami```
Output:
```app```
4. Check the application responsiveness
Command:
```curl localhost:5000```
Output:
GitOps demo app is running
5. Check the release version
Command:
```curl localhost:5000/version```
Output:
```v1```

See the [Dockerfile](./app/Dockerfile) for the container configuration.

<details>
<summary>Reproducing the full pipeline (condensed)</summary>

- kind create cluster --name gitops-demo
- Create a GHCR pull secret (classic PAT with read:packages — see Troubleshooting Notes)
- kubectl apply -f manifests/
- Install Argo CD (see official docs — Server-Side Apply required, see Troubleshooting Notes)
- Point an Argo CD Application at this repo's manifests/ folder
</details>

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

### Docker permission in WSL

During the initial setup, Docker and kind commands required ```sudo```. 
The issue was that the current Linux user was not part of the ```docker``` group.

To fix it, there are 2 solutions :
1. Write ```sudo``` before every docker-touching 
2. Add the user docker to the group

The second approach is more practical.
Add the current user to the Docker group:
```sudo usermod -aG docker $USER```
After logging out and back in, or restarting the WSL session, verify the user's groups:
```groups```

### GHCR fine-grained token issue

During the deployment, the pod failed with a 401 Unauthorized error: ```Failed to pull image "ghcr.io/nirvops/gitops-argocd-demo```.

The issue was that since the GHCR image is private and no imagePullSecret had been configured, the pull attempt was unauthenticated.

To fix it, the solution was to add a kubernetes secret containing the PAT, and referenced it via imagePullSecrets in the deployment spec. 

The issue then changed into a 403 Forbidden one. The fine-grained PAT don't reliably work for GHCR pulls. To fix it, it was necessary to switch to classic PAT.

### Secret name mismatch

During the creation of the secret, the "already exists" error appeared.

The issue : create a new secret with the same name as an earlier one (```ghcr-secret```) failed because it already existed.

The fix required two steps: renaming the secret to ```ghcr-pull-image-secret```, then updating the imagePullSecrets reference in the manifest to match. The old secret was deleted afterward to avoid confusion.

### ArgoCD CRD issue

During the deployment, the Argo CD CRD "too long" install error appeared.

The issue was that kubectl apply failed on applicationsets.argoproj.io due to the 262144-byte annotation limit.

To fix it, the arguments --server-side --force-conflicts has been added to the command. This shifts the apply logic from the client (kubectl computing the diff locally) to the API server itself, avoiding the local last-applied-configuration annotation that was hitting the 256KB limit.

## Future Improvements

- Replace the hard-coded kubernetes manifest with an automated one.
- Replace local Kubernetes with a managed Kubernetes cluster.
- Add GitHub webhook integration to reduce Git reconciliation latency.
- Allow ArgoCD to automatically synchronize the cluster 
- Introduce Helm or Kustomize for environment-specific configuration.
- Add Prometheus/Grafana for monitoring and observability.
- Add automated security scanning for container images.

## Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| Application | Python | Sample application |
| Containerization | Docker | Build the application image |
| CI | GitHub Actions | Build and publish the image |
| Container Registry | GHCR | Store container images |
| CD / GitOps | Argo CD | Synchronize Kubernetes resources |
| Orchestration | Kubernetes | Run the application |
| Local Kubernetes | kind | Local Kubernetes cluster |
| Development Environment | WSL2 / Ubuntu | Local development environment |
| Version Control | Git / GitHub | Source code and desired state |

PS: 
*Scale example: If you wish to test the pipeline, feel free to play with the replicas in the deployment file.*

GitHub Actions | Kubernetes | Argo CD | Docker | GitOps