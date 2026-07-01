# GitOps CI/CD pipeline using Argo CD and GitHub Actions — automated deployment to Kubernetes on every push

<!-- ONE LINE: what this is, no fluff. Fill in once scope is locked. -->
<!-- e.g. "GitOps CI/CD pipeline using Argo CD and GitHub Actions — automated deployment to Kubernetes on every push." -->

## Architecture

<!-- PLACEHOLDER — do not fill until the pipeline actually runs end to end.
Draw the real flow, not the intended one. If the real flow has a manual step
you haven't automated yet, the diagram should show that honestly. -->

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

<!-- PLACEHOLDER — fill in last. This is the section that separates you
from a copy-pasted tutorial repo. What did you deliberately not build?
What would break in production? Say it plainly. -->
