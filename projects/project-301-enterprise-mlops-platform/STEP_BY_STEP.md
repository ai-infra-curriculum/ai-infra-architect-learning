# Enterprise MLOps Platform — Step-by-Step Build Guide

> Project 301 | 80 hours total, organized as an 11-week part-time build
> Companion to `architecture.md`. Read that first.

This guide walks a learner from an empty AWS account to a working multi-tenant
MLOps platform that hosts at least one tabular model and one LLM endpoint, with
lineage, audit, and FinOps wiring intact. Where full enterprise-scale build-out
would cost real money, the guide gives you a "lite" path that exercises the same
control loops at low cost (target ≤ $400 of AWS spend for the entire project if
you tear down nightly).

---

## Pre-Requisites Checklist

Before week 1, make sure you have:

- [ ] An AWS account where you have admin or near-admin access. A throwaway sub-
      account in an AWS Organization is ideal.
- [ ] A budget alarm in that account at $50, $150, $300 (you should never get a
      $300 alarm if you tear down nightly).
- [ ] CLI tools installed locally:
  - `aws` v2.15+
  - `kubectl` matching EKS 1.30 (server skew ≤ 1)
  - `helm` v3.14+
  - `terraform` v1.7+ (or OpenTofu 1.6+)
  - `eksctl` v0.180+ (optional)
  - `argo` CLI 3.5+
  - `mlflow` 2.14
  - `cosign` 2.x
  - `trivy` 0.50+
  - `kustomize` v5+
  - `jq`, `yq`, `gh`
- [ ] A GitHub organization with at least one private repo. The platform uses
      GitHub Actions and GitHub OIDC for keyless AWS auth.
- [ ] A free-tier Okta developer org **or** a Keycloak in Docker (if you don't
      want Okta, the guide notes the substitutions).
- [ ] Python 3.12 and Go 1.22 toolchains locally.
- [ ] Basic familiarity with Kubernetes (you can `kubectl get pods` and read a
      YAML), Helm, and at least one ML framework (PyTorch or sklearn).

### Recommended reading before starting

- *Designing Machine Learning Systems*, Chip Huyen (Chapters 7–10)
- AWS EKS Best Practices Guide — sections on networking, IAM, security
- KServe documentation — "Inference Service" + "Model Mesh"
- OpenLineage spec — events and namespacing
- The full `architecture.md` of this project

### Cost ceiling for the learning build

| Phase | Approx. spend if torn down nightly | Notes |
|-------|-----------------------------------|-------|
| 1 | $40 | One small EKS, no GPU |
| 2 | $90 | Adds Aurora Serverless v2, S3, KMS |
| 3 | $120 | Adds a g5.xlarge spot for one GPU experiment |
| 4 | $80 | Online serving, Redis t4g.small |
| 5 | $70 | Multi-tenant + audit demo |
| **Total** | **~$400** | Set the $300 alarm; if it fires, you forgot to destroy something |

---

## Phase 1 — Foundation (Week 1, ~10 hrs)

### Phase 1 goals

- Stand up the AWS substrate: VPC, EKS, IAM roles, ECR, KMS, S3.
- Wire GitHub OIDC so no static IAM keys ever live on your laptop or in CI.
- Pass the CIS EKS benchmark on an empty cluster.

### Day 1 — Repo + VPC + KMS (2 hr)

1. Create `mlops-platform-infra` repo. Initialize with `terraform/` directory.
2. Configure Terraform remote state in S3 with DynamoDB locking. Use a separate
   `bootstrap/` Terraform module to create the state bucket and lock table.
3. Write `terraform/network.tf`:
   - VPC `10.20.0.0/16`
   - Three private subnets (`/20`) across three AZs in `us-east-1`
   - Three public subnets (`/24`) for the NAT gateways and ingress LBs
   - VPC endpoints for `s3`, `ecr.api`, `ecr.dkr`, `kms`, `sts`, `logs`
4. Write `terraform/kms.tf`:
   - One CMK for EBS encryption
   - One CMK for S3 artifact bucket
   - One CMK for secrets (used by EKS Secrets encryption)
5. Plan and apply.

**Validation**: `aws ec2 describe-vpcs` shows the VPC, `aws kms list-keys` shows
the three CMKs.

### Day 2 — EKS + Karpenter (3 hr)

1. Use the `terraform-aws-modules/eks/aws` module (v20+). Create one EKS 1.30
   cluster `mlops-mvp`.
2. Enable cluster logging (api, audit, authenticator) → CloudWatch.
3. Add one initial managed node group (2x `m6i.large`, on-demand) for system
   workloads.
4. Install Karpenter v1.0 via Helm; create one `NodePool` `general-cpu`
   (m6i.large, m6i.xlarge, mixed spot+on-demand).
5. Verify Karpenter provisions a node by submitting a `Deployment` with 10
   replicas requesting 0.5 CPU each.

**Gotchas**:

- Karpenter `EC2NodeClass` needs an instance profile; the module doesn't always
  create one. Create it explicitly.
- Don't put system pods (CoreDNS, Karpenter itself) on Karpenter-managed nodes.
  Keep them on the managed node group.

### Day 3 — IAM, GitHub OIDC, ECR (2 hr)

1. Create an IAM OIDC provider for `token.actions.githubusercontent.com`.
2. Write reusable IAM roles bound to specific GitHub orgs/repos/branches/
   environments. Trust policy example:
   ```json
   {
     "Effect": "Allow",
     "Principal": { "Federated": "arn:aws:iam::ACCT:oidc-provider/token.actions.githubusercontent.com" },
     "Action": "sts:AssumeRoleWithWebIdentity",
     "Condition": {
       "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
       "StringLike": { "token.actions.githubusercontent.com:sub": "repo:techcorp/*:environment:platform-dev" }
     }
   }
   ```
3. Create ECR repos: `mlops/platform-api`, `mlops/feast-server`, `mlops/training-base`.
4. Verify keyless push from a GitHub Actions workflow.

### Day 4 — Baseline security + benchmark (3 hr)

1. Install AWS Load Balancer Controller and ExternalDNS.
2. Install cert-manager.
3. Install kube-bench as a Job; address findings until you pass the EKS profile.
4. Install Falco for runtime monitoring (low-volume rules only for now).

### Phase 1 deliverables

- [ ] `mlops-platform-infra` repo with green CI
- [ ] EKS cluster you can `kubectl get nodes` against
- [ ] Karpenter scaling a synthetic workload successfully
- [ ] CIS EKS benchmark: zero high/critical findings
- [ ] GitHub Actions deploys via OIDC, no static AWS keys committed

### Phase 1 failure modes

- "My subnets have no route to the internet" — you forgot the NAT gateway
  associations on the private RT.
- "Karpenter logs 'unable to launch instances'" — almost always missing IAM
  permissions on the node IAM role or wrong subnet tagging
  (`karpenter.sh/discovery=mlops-mvp`).
- "EKS endpoint refusing OIDC tokens" — `aws eks describe-cluster` and check
  that `identity.oidc.issuer` matches what you registered.

---

## Phase 2 — Control Plane MVP (Weeks 2–3, ~15 hrs)

### Phase 2 goals

- Stand up MLflow, the Platform API skeleton, and OPA.
- Wire Okta (or Keycloak) for human SSO.
- Make one end-to-end project lifecycle work: create project → register model.

### Day 1 — MLflow (2 hr)

1. Create an Aurora Postgres Serverless v2 cluster (min 0.5 ACU, max 2 ACU).
2. Create an S3 bucket `techcorp-mlops-artifacts-${ACCT}` with KMS-CMK SSE,
   block-public-access, versioning, lifecycle to IA at 90d.
3. Helm install `community-charts/mlflow` 0.7+ with:
   - Backend: the Aurora Postgres DSN (use AWS Secrets Manager + External
     Secrets Operator to inject).
   - Artifact store: the S3 bucket; configure IRSA for the MLflow ServiceAccount.
4. Expose via an internal ALB on `mlflow.platform.internal`.

**Validation**: `mlflow experiments search` from the CLI returns the default
experiment.

### Day 2 — Okta + OAuth2 Proxy (3 hr)

1. In Okta, create an OIDC web app for the platform.
2. Deploy `oauth2-proxy` in front of MLflow and (later) Backstage; use Okta as
   the IdP, write group claims into headers (`X-Auth-Request-Groups`).
3. Verify only authenticated Okta users can reach MLflow.

If using Keycloak instead of Okta, the steps are identical; just point
oauth2-proxy at the Keycloak realm.

### Day 3–4 — Platform API skeleton (5 hr)

1. Create `platform-api` repo. Scaffold FastAPI 0.110, SQLAlchemy 2, Alembic.
2. Domain model:
   ```python
   class Project(Base):
       id: UUID
       name: str  # unique within tenant
       tenant_id: str
       cost_center: str
       risk_class: Literal["minimal","limited","high","unacceptable"]
       created_at: datetime
       owners: list[str]  # Okta group DNs

   class Run(Base):
       id: UUID
       project_id: UUID
       mlflow_run_id: str
       status: Literal["queued","running","succeeded","failed"]
       git_sha: str
       container_digest: str
       started_at: datetime
       ended_at: datetime | None
   ```
3. Endpoints: `POST /v1/projects`, `GET /v1/projects/{id}`, `POST /v1/runs`,
   plus an internal `POST /v1/events` for lineage.
4. AuthN middleware reads `X-Auth-Request-*` headers from oauth2-proxy; AuthZ
   checks group membership against project owners.
5. Containerize, push to ECR, deploy as a `Deployment` + `Service` + ALB Ingress.
6. Smoke test with `httpie` or `curl`.

**Gotchas**:

- Don't put the Platform API on the public internet. Use an internal ALB and
  reach it via a VPN or `kubectl port-forward` during the build.
- Use OpenAPI from FastAPI to generate a Go client for the `mlctl` CLI later.

### Day 5 — OPA + first policy (3 hr)

1. Install Gatekeeper.
2. Write ConstraintTemplate `mlops-required-labels`: any Deployment in a
   tenant namespace must carry `tenant`, `cost-center`, `risk-class` labels.
3. Write ConstraintTemplate `mlops-image-from-allowed-registries`: containers
   must come from `*.dkr.ecr.us-east-1.amazonaws.com/mlops/*` or
   `ghcr.io/techcorp/*`.
4. Drop OPA into the Platform API as a sidecar (REST mode); add an
   `/v1/policy/evaluate` route that delegates to OPA.

### Day 6 — `mlctl` CLI (2 hr)

1. Create `mlctl` Go repo. Use `cobra` + `viper`.
2. Commands: `mlctl projects list|create`, `mlctl runs submit`, `mlctl auth
   login` (browser-based device flow against Okta).
3. Generate the API client from the OpenAPI doc with `oapi-codegen`.
4. Ship a single static binary via `goreleaser`.

### Phase 2 deliverables

- [ ] MLflow tracking server reachable via Okta SSO
- [ ] Platform API can create a Project and a Run, and surfaces them via REST
- [ ] OPA blocks a deployment missing required labels (demonstrate the deny)
- [ ] `mlctl` can authenticate and list projects
- [ ] Aurora + S3 are tagged for cost attribution

### Phase 2 failure modes

- Aurora "cannot connect" — check security groups and that the SG of the EKS
  node-group is in the Aurora SG ingress on 5432.
- MLflow "permission denied on s3" — IRSA misconfigured; verify the SA
  annotation matches the IAM role ARN and the role's trust policy lists the SA.
- oauth2-proxy returns 500 after Okta callback — almost always the cookie
  secret is wrong length (must be 16, 24, or 32 bytes).

---

## Phase 3 — Training Engine (Weeks 4–5, ~15 hrs)

### Phase 3 goals

- Run a real training job that produces a registered MLflow model with full
  lineage to OpenLineage.
- Get one GPU experiment working under Karpenter on spot.
- Demonstrate Ray distributed training on a small scale.

### Day 1 — Argo + Kubeflow Pipelines (3 hr)

1. Install Argo Workflows 3.5 with the workflow-controller in cluster-scope mode
   for the platform namespace and tenant namespaces.
2. Install Kubeflow Pipelines 2.x standalone (skip the full Kubeflow deployment).
3. Run the `hello-world` KFP example.

### Day 2 — Reference training pipeline (3 hr)

1. Create `cookiecutter-training-tabular` template repo. The template produces:
   - `pipeline.py` (KFP v2 definition): `load → preprocess → train → evaluate
     → register`
   - `Dockerfile` based on `pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime`
   - `model_card.md` template
   - `eval.py` with required slice metrics
2. Run the pipeline end-to-end on a sample dataset (the OpenML "adult" dataset
   is a fine test).
3. Validate the registered model shows up in MLflow with metrics, the model
   card is attached, and the OpenLineage events landed in Marquez.

### Day 3 — OpenLineage + Marquez (2 hr)

1. Deploy Marquez (Postgres + API + web UI) on the cluster.
2. Configure the KFP pipeline to emit OpenLineage events using
   `openlineage-airflow` style hooks (or call the OpenLineage HTTP API directly
   from each step's pre/post hooks).
3. Verify in the Marquez UI that the run lineage is complete: input dataset →
   step containers → output model.

### Day 4 — Karpenter GPU pool (2 hr)

1. Add a new `NodePool` `gpu-spot`:
   - Instance types: `g5.xlarge`, `g5.2xlarge`, `g5.12xlarge` (A10G)
   - Capacity type: `spot`
   - Taint: `nvidia.com/gpu=true:NoSchedule`
2. Install the NVIDIA k8s device plugin.
3. Submit a tiny training job (1 epoch, 1 GPU, ResNet18 on CIFAR-10) and
   verify it lands on a g5.xlarge spot node.

**Gotchas**:

- Spot quotas in a new account are often **zero**. Request a quota increase
  before this day or you'll spend an afternoon staring at "InstanceLimitExceeded".
- The NVIDIA device plugin needs the `nvidia` runtime; in EKS this is provided
  by the GPU-optimized AMI. Make sure your NodePool's `EC2NodeClass` selects
  the right AMI (`amiSelectorTerms` with `eks-optimized-gpu`).

### Day 5 — Ray on Kubernetes (3 hr)

1. Install KubeRay operator.
2. Submit a `RayJob` that fans out a small data-parallel training job across
   2 workers × 1 GPU.
3. Demonstrate spot-checkpoint-restore: kill a Ray worker mid-training and
   show the job recovers from the last checkpoint written to S3.

### Day 6 — Promote → Production canary (2 hr)

1. Add the promotion policy to the Platform API: a `POST /v1/models/{id}/
   promote` route that checks (a) eval report present, (b) image scan ≤ HIGH,
   (c) two-person approval, then sets the MLflow stage.
2. Write the OPA policy in Rego.
3. Walk through a manual promotion of your trained model from Staging to
   Production.

### Phase 3 deliverables

- [ ] One full pipeline run (KFP) registered in MLflow
- [ ] Marquez shows complete lineage for that run
- [ ] A GPU training job ran successfully on a g5 spot node
- [ ] A Ray distributed run survived a worker eviction
- [ ] A model promoted from Staging → Production via the Platform API with
      OPA-enforced gates

### Phase 3 failure modes

- KFP `argo-server` returns 403 — RBAC; the `pipeline-runner` SA needs
  permissions on Argo Workflow CRDs.
- "PodGroup pending due to taints" — you tainted the GPU pool but forgot to
  add the matching toleration to the training pod spec.
- Ray actors die silently with no logs — almost always memory; lower batch
  size or pick a larger node.
- MLflow stage transition fails — likely you didn't run `mlflow db upgrade`
  after pulling a newer MLflow version.

---

## Phase 4 — Online Serving + Feature Store (Weeks 6–7, ~15 hrs)

### Phase 4 goals

- Deploy a real model behind KServe with mTLS, autoscaling, and a canary split.
- Stand up Feast (offline + online) and serve features at < 10 ms p99.
- Add an LLM endpoint with vLLM.

### Day 1 — KServe install + first endpoint (3 hr)

1. Install Knative Serving (just the serving part).
2. Install KServe 0.13.
3. Create an `InferenceService` for your tabular model using the `sklearn`
   predictor (point at the MLflow S3 artifact URI). Test with `curl`.
4. Add Istio injection on the namespace; verify mTLS between Knative
   activator and the predictor pod.

### Day 2 — Triton multi-model packing (2 hr)

1. Re-deploy the model on the Triton runtime. Pack a second model on the
   same `InferenceService` using model-mesh.
2. Compare cost per 1k predictions vs. one-pod-per-model.

### Day 3 — Feast offline + online (3 hr)

1. Define a Feast repo with one `FeatureView` over a small Iceberg/Parquet
   table on S3.
2. Materialize to Redis (ElastiCache `cache.t4g.small`).
3. Benchmark online lookups with `vegeta` or a tiny Python client; record p50/
   p95/p99.

### Day 4 — Wire features into the model (2 hr)

1. Modify the inference path to fetch features from Feast online before
   prediction.
2. Add per-request OpenTelemetry tracing; visualize one trace in Tempo +
   Grafana that spans Istio ingress → KServe → Feast → predictor → response.

### Day 5 — vLLM endpoint (3 hr)

1. Add a g5.12xlarge or g6.12xlarge NodePool for LLM serving (on-demand for
   this experiment to avoid spot reclaim mid-demo).
2. Deploy a small open-weights model (e.g., Llama-3-8B-Instruct) on vLLM 0.5
   behind a KServe `InferenceService` (custom predictor).
3. Test with `openai`-style client (`v1/chat/completions`).

### Day 6 — Canary traffic split (2 hr)

1. Train a v2 of your tabular model with slightly different hyperparameters.
2. Use KServe's `canaryTrafficPercent` to send 10% of traffic to v2.
3. Validate prediction-distribution drift in Evidently dashboards.

### Phase 4 deliverables

- [ ] Tabular model live, ≥ 100 RPS with p95 ≤ 80 ms
- [ ] Two models packed on one Triton instance with cost numbers in your notes
- [ ] Feast online p99 ≤ 10 ms
- [ ] One end-to-end trace in Tempo showing all hops
- [ ] vLLM serving Llama-3-8B with token streaming
- [ ] Canary v1/v2 split working

### Phase 4 failure modes

- KServe 503 — Knative activator can't reach predictor; check Istio sidecar
  is injected and the SA has the right `peerAuthentication`.
- Feast online returns `feature not found` — you materialized to an older
  registry; bump the registry version and re-deploy.
- vLLM OOM at startup — wrong `--max-model-len`; tune relative to GPU VRAM
  (Llama-3-8B at fp16 on a 24 GB A10G typically needs `--max-model-len
  4096`).
- "AZ imbalance" warnings on KServe — set `topologySpreadConstraints` with
  `maxSkew: 1` across `topology.kubernetes.io/zone`.

---

## Phase 5 — Cross-cutting & multi-tenant (Weeks 8–10, ~20 hrs)

### Phase 5 goals

- Multi-tenant isolation that actually holds up to a red-team check.
- Observability you'd be willing to run on-call against.
- Cost attribution down to per-run and per-1k-predictions.
- An audit lake demo.

### Day 1–2 — Tenant model + namespaces (4 hr)

1. Define two tenants: `tenant-fraud` and `tenant-fcst`. Create namespaces with:
   - Default-deny `NetworkPolicy`
   - Tenant-scoped `ResourceQuota` (CPU, memory, GPU)
   - Tenant `ServiceAccount` with IRSA-bound IAM role that can only touch
     `s3://techcorp-mlops-artifacts/${tenant}/*` and the tenant's KMS key.
2. Write a Kyverno policy that injects required labels (`tenant`, `cost-
   center`, `risk-class`) and rejects pods missing them.
3. Try a "noisy neighbor" attack: deploy a pod in `tenant-fraud` that tries
   to read from `tenant-fcst`'s S3 path. Confirm denial.

### Day 3 — Observability stack (4 hr)

1. Install kube-prometheus-stack (Prometheus + Grafana + Alertmanager).
2. Install Loki for logs and Tempo for traces (single binary mode is fine
   for the learning build).
3. Wire FastAPI Platform API, MLflow, and KServe predictors with the
   OpenTelemetry Python SDK exporting OTLP to Tempo.
4. Build a Grafana dashboard for one tier-1 model showing: throughput,
   latency p50/95/99, GPU utilization, prediction drift PSI, cost per 1k
   predictions.

### Day 4 — Multi-window multi-burn-rate SLO alerts (2 hr)

1. Define SLOs for the tabular model:
   - 99.95% availability over 30 days
   - 95% of requests under 80 ms
2. Implement multi-window multi-burn-rate alerts in Alertmanager
   (1h / 6h burn-rate windows, ticket vs. page severity).
3. Force a burn by introducing 5% error injection; verify alerts fire and
   recover correctly.

### Day 5 — Kubecost + unit-cost service (3 hr)

1. Install Kubecost (community edition) on the cluster.
2. Write a small Go service `unit-cost-svc` that:
   - Reads Kubecost allocations every 15 min
   - Joins them with Platform API run/deployment metadata
   - Materializes a table `cost_unit_metrics` (project, model, $/run,
     $/1k-predictions) in Postgres
3. Add a Grafana panel for $/1k-predictions, segmented by tenant.

### Day 6 — Audit lake (3 hr)

1. Create `techcorp-mlops-audit-${ACCT}` S3 bucket with Object Lock in
   compliance mode, 7-year retention.
2. Wire the Platform API to publish every state-mutating event to a Kinesis
   Firehose → S3 (JSON, partitioned `year=/month=/day=/`).
3. Glue + Athena: create a table over the audit lake and run a sample query
   ("show all production deployments by tenant-fraud in the last 30 days").
4. Implement the daily Merkle-chain digest job (Lambda) that hashes the
   prior day's partitions and writes the digest to a separate
   write-once-read-many bucket.

### Day 7 — Approval workflow (2 hr)

1. Add a `POST /v1/approvals` flow that puts a model promotion in a "pending
   approval" state and notifies a Slack channel (incoming webhook).
2. Build a tiny Backstage plugin (or just a CLI command) for an approver to
   approve / reject. Persist the decision in the audit lake.

### Day 8 — EU AI Act drill (2 hr)

1. Pick a "production prediction" event from your audit lake.
2. Walk the lineage backward via Marquez API → training run → input dataset
   versions → model card → approvers.
3. Time yourself. Target: ≤ 5 minutes.

### Phase 5 deliverables

- [ ] Two tenants with hard isolation; noisy-neighbor attempt blocked
- [ ] Grafana dashboard for tier-1 model that an on-call would actually use
- [ ] Functional SLO alerts (paged and recovered cleanly during induced burn)
- [ ] Unit-cost panel showing $/1k-predictions per tenant
- [ ] Audit lake queryable from Athena with daily Merkle digest
- [ ] Approval workflow gating model promotion to Production
- [ ] EU AI Act drill completed in ≤ 5 minutes

### Phase 5 failure modes

- "S3 access denied" from a tenant pod — almost always IRSA + KMS combined;
  the role can list/get S3 but the KMS key policy excludes the role.
- Kubecost shows $0 — install ran but Prometheus retention is too short;
  Kubecost needs at least 24 h to produce useful numbers.
- Object Lock in compliance mode is permanent. Use governance mode while
  learning. Compliance mode in prod only after you're sure.
- Alertmanager doesn't page — Slack webhook works but PagerDuty integration
  needs the routing key. Test in staging first.

---

## Phase 6 — Final integration & demo (Week 11, ~5 hrs)

### Goals

- Tell a coherent story end-to-end. Show the audit, the cost, the lineage,
  the rolling deployment, the SLO.

### Demo script (the one you'd actually give to an exec sponsor)

1. **0:00** — Show Backstage catalog. Pick one production model.
2. **0:30** — Click into model card. Show risk class (EU AI Act), eval
   metrics, approvers, last deployment timestamp.
3. **1:30** — Open the Grafana scorecard panel. Show p95 latency, drift
   PSI, $/1k-predictions trending over 30 days.
4. **3:00** — Show a candidate v2 in Staging. Promote with `mlctl model
   promote`. OPA gate fires asking for second approver; complete in Slack.
   Show the canary going 10% → 50% → 100%.
5. **5:00** — Trigger the EU AI Act drill: pick a prediction at random
   from the audit lake, click through to the model, training run, lineage,
   and approver list. Stopwatch.
6. **7:00** — Open the cost dashboard. Show fleet GPU utilization and
   per-tenant spend.
7. **8:00** — Open the Karpenter + Spot dashboard. Show the spot reclaim
   resilience numbers.
8. **9:00** — Q&A.

### Final deliverable artifact

- A 12-slide deck summarizing the architecture
- A 5-minute screen recording of the demo above
- The 10+ ADRs in `src/adrs/`
- A FY1 cost projection in `docs/COST-MODEL.md`
- A runbook in `docs/DEPLOYMENT.md` covering deploy, rollback, and incident
  triage

---

## Stretch Goals

If you finish early or want to dig deeper, pick from:

- **Multi-cluster federation** with Karmada or Cluster API for the warm-
  standby region. Implement Route 53 weighted records flip with a runbook.
- **Capacity Blocks for ML**: write a small service that reserves capacity
  blocks based on queued jobs and exposes the reserved window via the
  Platform API.
- **Kueue + Volcano**: switch the training engine to Kueue (preemption,
  priority, fair-sharing) and run a tenant-noisy-neighbor scenario.
- **Model Mesh density tuning**: pack 50+ low-traffic models on one Triton
  pod and measure aggregate cost vs. one-per-pod.
- **SLSA-3 with in-toto**: prove every artifact's provenance by generating
  in-toto attestations on every build and verifying at admission.
- **Right-to-explanation hook**: add SHAP at the inference path for tabular,
  and persist explanations to the audit lake.
- **Bias drill**: introduce a biased training set on purpose. Demonstrate
  Fairlearn slice metrics catching it during promotion.
- **Cost anomaly detection**: a small isolation-forest on the unit-cost
  metrics that alerts on regressions.

---

## Common Failure Modes During Build (cross-phase)

These bite repeatedly. Read once, save yourself a week of debugging.

### Networking

- Pods can resolve DNS but cannot reach the internet → NAT gateway is in
  the wrong AZ relative to the subnet route table.
- VPC endpoints don't help your pod → endpoint policy too restrictive, or
  pod is using the public DNS (`s3.amazonaws.com`) instead of the regional
  endpoint.

### IAM

- IRSA "AccessDenied" even though the role looks right → the SA annotation
  needs the *exact* role ARN; trust policy needs the *exact* SA in the form
  `system:serviceaccount:<ns>:<sa>`; the SA must exist before the pod starts.
- Cross-account assume-role fails → check the trust policy `Condition` for
  `aws:PrincipalTag` vs. `sts:RoleSessionName`.

### Kubernetes / Karpenter

- Pods stuck in `Pending` with `0/0 nodes available` → Karpenter logs are
  your friend. Most often: pool selector mismatch (the pod's nodeSelector
  doesn't match any pool's labels).
- Spot reclaim cascades → too few instance types in the pool; widen
  `instanceTypes` to give the fleet flexibility.

### MLflow / Tracking

- `mlflow.log_model` works locally but fails in CI → the CI pod's IAM role
  doesn't have `s3:PutObject` on the artifact bucket, **or** the KMS key
  policy doesn't allow it to encrypt.
- "experiment not found" — the run was logged against a different tracking
  server URI; check `MLFLOW_TRACKING_URI`.

### Serving

- KServe `RevisionFailed` — almost always the predictor image can't be
  pulled (ECR auth) or the storage initializer can't read S3 (IRSA again).
- vLLM "CUDA out of memory" on a model that should fit — `--gpu-memory-
  utilization` defaults to 0.9 and you have other GPU-using pods on the
  node. Either pin the node or tune the fraction.

### Observability

- Prometheus disk fills overnight → cardinality. Search for the worst
  series with `topk(50, count by (__name__) ({__name__=~".+"}))` and add
  `metric_relabel_configs` drops.
- Tempo traces don't connect across services → missing `traceparent` header
  propagation; common offender is a middleware that drops headers.

### Cost

- The bill spiked overnight → NAT gateway egress. Cross-AZ traffic and
  unintended internet egress are the top two surprises. Tag everything and
  use CUR + Athena to find the culprit.
- Karpenter consolidation never runs → `disruption.consolidationPolicy`
  defaults you might not want; set it explicitly.

---

## When you finish

- Tear down ALL the resources. Run `terraform destroy` and visually verify
  in the AWS console that EKS, Aurora, ElastiCache, S3 buckets (after
  emptying), and KMS keys (scheduled for deletion) are gone.
- Archive the repo, deck, and recording in your portfolio.
- Write a one-page reflection: which architectural decisions changed during
  the build vs. design, and why.

**You now have shipped, in miniature, the same control loops a Fortune 500
MLOps platform team operates at production scale.**
