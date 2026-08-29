# GitOps CI/CD pipeline using Argo CD and GitHub Actions — automated deployment to Kubernetes on every push

<!-- ONE LINE: what this is, no fluff. Fill in once scope is locked. -->
<!-- e.g. "GitOps CI/CD pipeline using Argo CD and GitHub Actions — automated deployment to Kubernetes on every push." -->

## Architecture

The architecture of this project is based on a local PC, on the OS ubuntu 26.04. The first steps of the infra structure was the installation of docker kind (v0.24.0)

## Why these tools

<!-- PLACEHOLDER — fill this in AS you hit each decision, not after.
Prompts to answer when you actually face them:
- Why Argo CD over Flux (or over just `kubectl apply` in CI)?
- Why kind over minikube/k3d?
- Pull-based sync vs push-based deploy — what did you actually pick, and what
  did that decision cost you (latency? complexity? something else)?
Write your answer the day you make the decision. If you can't explain why
you didn't pick the alternative, you don't understand the decision yet —
that's a signal to go learn the alternative, not to skip the question. -->

## What this demonstrates

<!-- Safe to draft now, in general terms, since this maps to skills not
implementation details. Tighten the wording once the repo is done. -->
- Declarative, Git-as-source-of-truth deployment (GitOps)
- Separation of build (CI) from deploy (CD) concerns
- Kubernetes manifest management via Argo CD

## Repo structure

<!-- Fill in as folders get created. Keep it accurate — a structure section
that doesn't match the actual repo is worse than no structure section. -->
```
.
├── app/            #
├── manifests/       #
├── .github/workflows/  #
└── README.md
```

## Running it locally

<!-- PLACEHOLDER — write these steps by literally running them yourself,
copy-pasting from your own terminal history, not from memory. If a step
doesn't work when you re-run it clean, the README is wrong, not the reader. -->

## Known limitations


## Troubleshooting Notes

### Installations

During the installation. I've noticed that for every command with docker and kind, the 'sudo' was necessary. When I was doing a command without it, the output was mostly empty. After a short troubleshooting (with Claude AI), the reason has been discovered.
When I was doing the groups command sudo was there but docker wasn't. The reason : I didn't know that I had to run the usermod command.
To fix it, there was 2 solutions that has been proposed to me. First write sudo before every docker-touching or add docker to the group list to run the commands without sudo. The most practical was of course the second one. 
The next step was then to do it using the command:
```sudo usermod -aG docker $USER```
Then close and reopen the terminal and check if docker was added to the groups:
```groups```

