# Multi-Cloud AI Infrastructure — Step-by-Step Build Guide

> Project 302 | 100 hours total, organized as a 12-week part-time build
> Companion to `architecture.md`. Read that first.

This guide walks a learner from three empty hyperscaler trial accounts to a
working three-cloud platform that can: (a) survive the kill of one cloud-region
without dropping tier-1 traffic, (b) place a training burst on the
cheapest-available accelerator pool, and (c) prove EU data residency for a
designated tenant. The full enterprise design costs real money; this guide
walks the same control loops at "lite" scale so that the entire 12 weeks fits
inside roughly $700 of total cloud spend when you tear down nightly.

---

## Pre-Requisites Checklist

Before week 1 you must have:

- [ ] **Three cloud accounts** with at least billing-admin: AWS, GCP, Azure.
      Use trial credits where you can. OCI is optional and can be skipped if
      you don't have an account; substitute a second GCP region.
- [ ] **Budget alarms in every account** at $50, $150, $300. If a $300 alarm
      fires you forgot a `tofu destroy`.
- [ ] **One organization in GitHub** with at least three private repos.
      Multi-cloud OIDC binds to repo and environment claims.
- [ ] **Cloudflare account** (free tier) with one domain you control (a
      `~$10/year` `.dev` works). DNS must be moved to Cloudflare.
- [ ] **Megaport sandbox or skip** — Megaport NaaS is the production answer for
      private cross-cloud; the lab uses IPsec or public-internet meshing.
- [ ] **CLI tools installed locally** (versions pinned):
  - `aws` 2.15+, `gcloud` 480+, `az` 2.60+, `oci` 3.40+ (optional)
  - `kubectl` 1.30 (server skew ≤ 1 against EKS 1.30 / GKE 1.30 / AKS 1.30)
  - `helm` 3.14+
  - `tofu` 1.6+ (OpenTofu; `terraform` 1.7+ also fine)
  - `crossplane` CLI 1.16+
  - `argocd` CLI 2.11+
  - `istioctl` 1.22+
  - `spire-server` / `spire-agent` 1.9+
  - `vault` 1.16+
  - `cloudflared` 2024.5+
  - `jq`, `yq`, `gh`, `direnv`
- [ ] **Python 3.12** and **Go 1.22** locally.
- [ ] **Okta developer org** (free) OR Keycloak in Docker.
- [ ] You are comfortable reading another team's Terraform, K8s YAML, and BGP
      basics. If "BGP" makes you flinch, schedule a half-day to brush up before
      week 5.

### Recommended reading before starting

- *Designing Data-Intensive Applications*, Kleppmann — chapters on replication,
  consistency, and partitioning.
- *Building Multi-Cloud and Hybrid Cloud Solutions*, Hashicorp ebook (free).
- AWS Multi-Region Application Architecture whitepaper.
- GCP "Patterns for distributed applications" series.
- Azure Architecture Center — "Multi-cloud and hybrid" pillar.
- The full `architecture.md` for this project.
- CNCF SPIFFE/SPIRE concepts page.
- Cloudflare "Geo Routing with Load Balancing" docs.

### Cost ceiling for the lab build

| Phase | Approx. spend if torn down nightly | Notes |
|-------|------------------------------------|-------|
| 1 | $40 | AWS-only foundation |
| 2 | $80 | Second AWS region + Aurora Global |
| 3 | $140 | GCP cluster added, cross-cloud Megaport-or-IPsec, Polaris |
| 4 | $180 | Azure EU AKS + EU Data Boundary + Confidential Containers (CC) |
| 5 | $120 | OCI burst (or GCP second region) + capacity scheduler |
| 6 | $90 | Cross-cloud FinOps + observability stack |
| 7 | $50 | Game day + DR drill |
| **Total** | **~$700** | The $300 alarm should never fire |

---

## Phase 1 — Multi-Cloud Governance & Bootstrap (Week 1, ~8 hrs)

### Phase 1 goals

- Stand up the **governance scaffolding first**: tag taxonomy, OPA-in-CI for
  Terraform plans, repo skeleton, OIDC bindings to all three clouds.
- Bootstrap **AWS only** for now (primary cloud). Other clouds in later phases.

### Day 1 — Repo skeleton + tag taxonomy (2 hr)

1. Create three repos: `multicloud-infra` (Terraform), `multicloud-platform`
   (Crossplane XRDs + Argo apps), `multicloud-policy` (OPA / Conftest /
   Rego).
2. In `multicloud-infra`, lay out:
   ```
   modules/
     portable/{cluster,bucket,kv,database}/
     aws/{vpc,eks,s3,kms,iam}/
     gcp/{vpc,gke,gcs,kms,iam}/
     azure/{vnet,aks,blob,kv,id}/
     oci/{vcn,oke,obj,kms}/
   envs/{aws-prod-east,aws-prod-west,gcp-prod-central,azure-eu-north}/
   bootstrap/
   ```
3. Define the **mandatory tag taxonomy** (`cost_center`, `tenant`,
   `workload_class`, `data_residency`, `risk_class`, `owner_email`) and write
   the first Conftest policy (`policy/required_tags.rego`) that fails any
   resource missing them.
4. Wire `pre-commit` and a GitHub Actions job `tofu-plan` that runs `tofu plan`
   and pipes the plan JSON into `conftest test` before any review.

**Validation**: open a PR adding a deliberately untagged resource. CI fails
with a clear "missing tag: cost_center" message.

### Day 2 — OIDC federation to all 3 clouds (3 hr)

1. AWS: create OIDC provider for `token.actions.githubusercontent.com`. Create
   three IAM roles (`multicloud-infra-readonly`, `multicloud-infra-plan`,
   `multicloud-infra-apply`) with trust conditions on
   `repo:org/multicloud-infra:environment:aws-prod-east`.
2. GCP: enable Workload Identity Federation; create a pool + provider for
   GitHub. Bind a service account `tf-deployer@proj.iam.gserviceaccount.com`.
3. Azure: register an app, configure federated credentials for the GitHub
   environment subject claim.
4. Run a smoke `tofu init` from a workflow in each environment; verify no
   static keys exist anywhere.

**Gotchas**:
- GitHub OIDC `sub` claim format differs for environments vs branches; for
  multi-cloud, **always use environments** so the format is uniform across
  clouds.
- Azure federated credentials cap at 20 per app — split per env.

### Day 3 — Bootstrap AWS primary network + KMS (3 hr)

1. Terraform `envs/aws-prod-east`:
   - VPC `10.30.0.0/16` across 3 AZs, private subnets `/20`, public `/24`.
   - Transit Gateway placeholder (single TGW; will attach prod-west later).
   - VPC endpoints for `s3, ecr.api, ecr.dkr, kms, sts, logs`.
   - One KMS CMK per data class: `cmk-secrets`, `cmk-artifacts`, `cmk-logs`.
2. Apply; capture outputs in remote state for cross-stack reference.

### Phase 1 deliverables

- [ ] Three repos with branch protection, CODEOWNERS, and Conftest CI gate
- [ ] OIDC federation working to AWS, GCP, Azure (no static keys)
- [ ] AWS primary VPC + TGW + KMS deployed and tagged
- [ ] `policy/required_tags.rego` enforced in CI

### Phase 1 failure modes

- "`Error: AccessDenied: not authorized to perform sts:AssumeRoleWithWebIdentity`"
  — your environment name in GitHub doesn't match the IAM trust condition
  exactly. Case-sensitive.
- WIF (GCP) returns "Permission 'iam.serviceAccounts.getAccessToken' denied"
  — you forgot `--member="principalSet://iam.googleapis.com/projects/.../attribute.repository/org/repo"`
  on the SA binding.

---

## Phase 2 — AWS Multi-Region Active-Active (Weeks 2–3, ~12 hrs)

### Phase 2 goals

- Add `prod-west` as a peer to `prod-east`. EKS in both. Aurora Global. S3 CRR.
- Cloudflare in front, with health-checked DNS failover.

### Day 1 — Second region VPC + TGW peering (2 hr)

1. Spin up `envs/aws-prod-west` mirroring east (CIDR `10.31.0.0/16`).
2. Peer the two TGWs (inter-region peering attachment).
3. Route tables: allow east ↔ west only for internal CIDRs; default still goes
   to local NAT.

### Day 2 — EKS in both regions (3 hr)

1. Use `terraform-aws-modules/eks/aws` v20+ in each region. Cluster name:
   `mc-east`, `mc-west`. K8s 1.30.
2. Install **Karpenter** in each. One `NodePool` `general-cpu` to start.
3. Confirm both clusters reachable via `kubectl` with separate kubeconfigs.

### Day 3 — Aurora Global DB (2 hr)

1. Create an Aurora PostgreSQL Global cluster. Primary in east, secondary
   read replica in west.
2. Failover drill (in-place): promote west → verify writes accepted there.
   Restore back to east. Time the drill (target ≤ 1 min handover).

### Day 4 — S3 cross-region replication + Cloudflare front (3 hr)

1. Create `multicloud-artifacts-east` and `-west`, both KMS-encrypted with
   separate CMKs (replication encrypts on the destination side with the
   destination CMK).
2. Enable bidirectional replication.
3. In Cloudflare:
   - Add `api.multicloud-lab.dev` as a CNAME to a Load Balancing pool.
   - Two origins: `east.api.multicloud-lab.dev` (ALB east),
     `west.api.multicloud-lab.dev` (ALB west).
   - Health check `/__lbcheck` returning 200 only if Aurora reachable.
   - Steering policy: geo + health.
4. Deploy a dummy `/__lbcheck` service on both clusters.

### Day 5 — First game day (2 hr)

1. Black-hole the east ALB by removing it from the Cloudflare pool.
2. Verify within 60 s traffic shifts to west.
3. Restore.
4. Document the exact wall-clock duration of impact in `docs/GAMEDAY-01.md`.

**Gotchas**:
- Aurora Global has a ~1-minute lag floor; do not assume zero RPO.
- If your `/__lbcheck` doesn't actually probe Aurora, the failover is
  cosmetic.

### Phase 2 deliverables

- [ ] Two EKS clusters in two AWS regions, both green
- [ ] Aurora Global with proven failover ≤ 1 min
- [ ] S3 CRR active both directions
- [ ] Cloudflare DNS with health-checked failover
- [ ] Game day write-up showing impact window

### Phase 2 failure modes

- TGW peering "Available" but pods can't reach across — you forgot to
  propagate routes; check route table associations on both attachments.
- Aurora Global failover that returns "Engine version mismatch" — the
  secondary was created on a different patch version.
- Cloudflare health check stays green during outage — health endpoint is
  trivially cacheable; add `Cache-Control: no-store`.

---

## Phase 3 — GCP Warm Standby + Cross-Cloud Mesh (Weeks 4–6, ~18 hrs)

### Phase 3 goals

- GKE in `us-central1` as a warm standby for tier-1.
- SPIRE federation between AWS and GCP.
- Istio multi-primary mesh across the two clouds.
- Iceberg + Polaris catalog spanning S3 and GCS.

### Day 1 — GKE bootstrap (2 hr)

1. `envs/gcp-prod-central`: enable VPC-native GKE 1.30, regional cluster
   `mc-gcp`, autopilot **off** (we want node pools we can control).
2. One node pool `general-cpu` with `e2-standard-4`, autoscaling 1–5.
3. Workload Identity enabled; bind a `KSA → GSA` mapping for the test app.

### Day 2 — Cross-cloud connectivity (3 hr)

For lab budget:
1. Spin up **IPsec tunnels** between AWS Site-to-Site VPN and Cloud VPN HA.
2. Production answer in your notes: Megaport NaaS via Direct Connect ↔ Cloud
   Interconnect.
3. Validate east-west reachability: a pod in `mc-east` can curl a pod in
   `mc-gcp` over private IP after appropriate K8s `Service` of type
   `LoadBalancer (internal)`.

### Day 3 — SPIRE servers + federation (4 hr)

1. Install SPIRE server in each cluster's `spire` namespace (Helm chart
   `spiffe/spire`).
2. Trust domains: `aws.techcorp.lab` and `gcp.techcorp.lab`.
3. Configure **SPIRE federation** via the federation API. Exchange trust
   bundles bi-directionally (one-time bootstrap; future refresh automatic).
4. Issue an SVID to a sample workload in each cluster. Use `spiffe-helper` to
   inject SVID into pod filesystem.
5. Demonstrate: a pod in AWS calls a pod in GCP using SPIFFE mTLS without any
   cloud-native identity exchange.

**Gotchas**:
- SPIRE federation requires reachable federation endpoints; ingress with TLS
  is mandatory. Cloudflare in front works.
- Trust-bundle refresh interval should be ≤ 5 min in lab to surface bootstrap
  bugs.

### Day 4 — Istio multi-primary (3 hr)

1. Install Istio 1.22 with the **multi-primary, multi-network** pattern.
2. East-west gateways on each cluster (NLB on AWS, ILB on GCP).
3. Mesh CA: integrate with SPIRE via the cert-manager-istio-csr bridge so
   workload certs come from SPIRE.
4. Deploy a `bookinfo`-style app split across clouds: `productpage` in AWS,
   `reviews` in GCP. Verify trace context end-to-end via traffic visualizer.

### Day 5 — Iceberg + Polaris (3 hr)

1. Polaris catalog (open source) in a small managed Postgres (RDS-east for
   the catalog metadata).
2. Create catalog entries pointing at `s3://multicloud-iceberg-east` AND
   `gs://multicloud-iceberg-central` as warehouse locations.
3. Use Spark or Trino on one of the EKS/GKE clusters to read/write an Iceberg
   table whose snapshots span both locations.
4. Demonstrate a **read replica**: write in AWS, read snapshot from GCP cluster.

### Day 6 — First cross-cloud failover game day (3 hr)

1. Force tier-1 service to consume from the GCP warm standby (DNS flip in
   Cloudflare).
2. Measure: RTO observed, error rate during cut, data correctness on the
   secondary.
3. Capture lessons in `docs/GAMEDAY-02.md`.

### Phase 3 deliverables

- [ ] GKE cluster running, peered to AWS over private connectivity
- [ ] SPIRE federation working end-to-end (a workload-to-workload call across
      clouds authenticated by SVIDs)
- [ ] Istio multi-primary mesh with locality-aware routing
- [ ] Polaris catalog and Iceberg tables readable from both clouds
- [ ] Documented cross-cloud failover within RTO 30 min

### Phase 3 failure modes

- "x509: certificate signed by unknown authority" between clouds — your
  Istio CA isn't trusting SPIRE; check the istio-csr issuer ref.
- Polaris returns 500 on table create — its Postgres can't reach the
  warehouse location; check IAM and the catalog service identity.
- Cross-cloud `ping` works but TCP hangs — MSS / MTU asymmetry on the VPN.
  Set `tcp-mss-clamping` on the tunnel.

---

## Phase 4 — Azure EU Sovereign Cell (Weeks 7–9, ~18 hrs)

### Phase 4 goals

- AKS in `northeurope` + `westeurope`, both **active-active** within the EU.
- **EU Data Boundary** enabled tenant-side.
- Sovereign Vault cluster in Azure; **separate trust domain** in SPIRE — no
  cross-boundary trust to AWS/GCP.
- Confidential Containers for the most sensitive workload.

### Day 1 — AKS bootstrap with EU Data Boundary (3 hr)

1. Subscription configured under EU Data Boundary.
2. AKS 1.30 in `northeurope` (`mc-az-n`) and `westeurope` (`mc-az-w`).
3. Azure CNI Overlay; Network Policy = Cilium for L7 policies.
4. Validate: every resource group is tagged `data_residency=eu_sovereign`.

### Day 2 — Sovereign Vault cluster + Azure Key Vault HSM (3 hr)

1. Deploy HashiCorp Vault Enterprise (or OSS for lab) into AKS-N. Storage =
   Azure Files w/ HSM-protected key.
2. Provision an Azure Key Vault **Managed HSM** for tenant BYOK material.
3. Document the key-generation ceremony in `docs/CEREMONY-EU.md`.

### Day 3 — Sovereign SPIRE trust domain (3 hr)

1. SPIRE in AKS-N with trust domain `eu.techcorp.sovereign`.
2. **Do NOT** federate this trust domain with AWS or GCP. Sovereign
   workloads stay sovereign.
3. Workloads in this trust domain can only call out to allowlisted
   destinations within the boundary.

### Day 4 — Confidential Containers (3 hr)

1. Enable AKS Confidential Containers (`--workload-runtime KataCcIsolation`).
2. Use a node pool with AMD SEV-SNP (DC-family) or Intel TDX VMs.
3. Wire **attestation**: a workload starts → emits an attestation token to
   Vault → Vault releases the tenant key only on valid attestation.
4. Demonstrate: tampering with the container image causes attestation to
   fail and Vault refuses the unwrap call.

### Day 5 — Sovereign log pipeline (3 hr)

1. Logs from AKS-N/W go to **Azure Monitor in EU regions only**. Verify with
   diagnostic settings.
2. Mirror cold storage to Azure Blob in EU; configure immutable WORM with
   `versionLevelImmutability`.
3. **No** forwarding to the US Grafana Cloud instance; use Grafana Cloud EU
   for the sovereign tenants.

### Day 6 — Sovereign tenant onboarding & geo-routing (3 hr)

1. In Cloudflare, add a Worker that inspects the JWT `tenant_id` claim and
   routes EU sovereign tenants to the AKS ingress.
2. Onboard `tenant-bank-fr` as the first sovereign tenant.
3. Run a synthetic data-flow audit (next phase) — for now, manually verify
   in Azure Monitor that the request never left the boundary.

### Phase 4 deliverables

- [ ] Two AKS clusters in EU, active-active, EU Data Boundary on
- [ ] Sovereign Vault + HSM with a documented key ceremony
- [ ] Sovereign SPIRE trust domain, isolated from US trust domains
- [ ] Confidential Containers workload with attestation-gated key release
- [ ] Sovereign log pipeline, EU-only
- [ ] One tenant routed only through the EU cell via Cloudflare Worker

### Phase 4 failure modes

- Attestation fails with no useful error — check the kata-agent logs; usually
  the platform attestation token has wrong audience.
- "Workload Identity token exchange failed" — federated credentials in Azure
  are bound to the SA name in a specific namespace; mismatch silently fails.
- A "sovereign" request still hits a US region — almost always the upstream
  CDN POP cached an asset in a US region; configure tiered cache with EU
  geos only.

---

## Phase 5 — OCI Burst + Capacity Scheduler (Week 10, ~12 hrs)

### Phase 5 goals

- Add OCI as a burst-only cloud for training (or skip OCI and use a second
  GCP region as the "fourth cloud" in the lab).
- Implement a small **capacity scheduler** that decides where to land a
  training job based on price × availability.

### Day 1 — OCI bootstrap (2 hr)

1. OCI tenancy, compartment `multicloud-lab`. VCN, OKE cluster
   `mc-oci-burst` with a tiny GPU node pool (`VM.GPU.A10.1`, optional).
2. Skip if you don't have OCI; replace with a third GCP region.

### Day 2 — Crossplane unified XRDs (3 hr)

1. Define an XRD `MLTrainingCluster` whose compositions on AWS produce
   EKS + Karpenter GPU pool, on GCP produce GKE + DWS, on OCI produce OKE
   + GPU node pool.
2. Demonstrate provisioning the **same intent** on two clouds.

### Day 3 — Capacity scheduler (4 hr)

1. Small Go service `cap-scheduler-svc`:
   - Pulls real-time accelerator pricing (AWS Spot pricing API, GCP
     pricing, OCI list price scraped from public docs).
   - Pulls availability signals (capacity reservation API where available;
     last-known-good probe otherwise).
   - On a job submit, picks the cheapest cloud satisfying constraints
     (region whitelist, residency, accelerator type, minimum reliability).
2. Wire to a queue. Run a 4-GPU `ResNet50` placeholder job: scheduler picks
   AWS first, then forces a "no-capacity" signal and confirm it re-routes
   to GCP.

### Day 4 — Job-placement transparency UI (3 hr)

1. Build a tiny dashboard (Grafana panel + a few promtail-fed events) that
   shows: job ID, candidate clouds, scores, chosen cloud, reason. Users
   should never wonder why their job landed where it did.

### Phase 5 deliverables

- [ ] OCI (or 4th GCP region) cluster operational
- [ ] One Crossplane XRD producing equivalent clusters on two clouds
- [ ] Capacity scheduler placing a synthetic job and re-routing on failure
- [ ] Transparency UI showing placement rationale

### Phase 5 failure modes

- Crossplane composition that works on AWS fails on GCP — XRD interface is
  too generic; you accidentally encoded an AWS-ism (e.g., "Subnet ID
  starting with subnet-").
- Capacity scheduler keeps picking the most expensive cloud — your spot
  price feed is wrong unit; AWS reports per-hour, GCP per-second, OCI
  monthly.

---

## Phase 6 — Cross-Cloud Observability & FinOps (Week 11, ~12 hrs)

### Phase 6 goals

- One Grafana pane. One ClickHouse for FinOps. Egress dashboard you trust.

### Day 1 — Grafana Cloud + Alloy (3 hr)

1. Grafana Cloud free tier; provision a stack.
2. Deploy Grafana Alloy in each cluster scraping Prometheus, Loki for
   logs, Tempo for traces.
3. Build a "multi-cloud overview" dashboard: cluster health, pod count,
   spot interruption rate per cloud, mesh east-west traffic.

### Day 2 — Cross-cloud trace propagation (2 hr)

1. Confirm W3C `traceparent` headers survive cross-cloud Istio hops.
2. Find one trace spanning AWS → GCP and visualize it in Tempo.

### Day 3 — FinOps ingest (4 hr)

1. Set up exports:
   - AWS CUR 2.0 → S3 Parquet hourly.
   - GCP Billing Export to BigQuery.
   - Azure Cost Management daily export to Blob.
   - OCI cost reports (CSV).
2. Land all four into ClickHouse via a dbt model with conformed dimensions
   (`cloud`, `region`, `service`, `tenant`, `cost_center`,
   `workload_class`, `accelerator_type`).
3. Build the "egress of the week" dashboard. Sort cross-cloud egress by
   tenant.

### Day 4 — Anomaly detection + per-tenant unit cost (3 hr)

1. Materialize `unit_cost_metrics` table: `$/run`, `$/1k-predictions`,
   `$/training-hour`, grouped by tenant and cloud.
2. Add an isolation-forest anomaly job that flags > 3σ daily deltas per
   tenant.
3. Demo: trigger an artificial 10× egress spike and confirm the alert
   fires inside 24 h.

### Phase 6 deliverables

- [ ] One Grafana pane covering all clouds
- [ ] One cross-cloud trace visualized
- [ ] ClickHouse FinOps model populated daily, all four billing sources
- [ ] Egress dashboard + anomaly alerts
- [ ] First weekly unit-cost report rendered to a PDF

### Phase 6 failure modes

- Cross-cloud trace missing the GCP span — Istio's tracing config in GCP
  uses a different sampler; align both to 100% during the lab.
- ClickHouse joins produce blanks — schema drift between CUR v1 and v2 is
  the usual cause; pin to one version in `dbt_project.yml`.

---

## Phase 7 — Final Game Day & Demo (Week 12, ~8 hrs)

### Game day script (end-to-end, ~2 hr)

1. **Setup**: pre-stage a 256-GPU job request (simulated; do not actually
   spin up 256 GPUs unless you really want to).
2. **Inject Failure A**: black-hole AWS us-east-1 egress. Verify tier-1
   service stays up on west + GCP within 30 min.
3. **Inject Failure B**: while A is healing, deliberately drop the SPIRE
   federation bundle on GCP. Validate that workloads in GCP can no longer
   call AWS endpoints (good — federation is the auth boundary).
4. **Capacity test**: submit the 256-GPU request. Scheduler picks OCI (or
   secondary GCP). Job is queued; show queue order and placement reason.
5. **Sovereign test**: send a request from `tenant-bank-fr`. Walk through
   the audit log proving it never left EU. Stopwatch the answer (target
   ≤ 5 min from question to evidence).
6. **Cost report**: open the FinOps dashboard, show MoM trend, show the
   biggest egress source last week, show the multi-cloud premium ratio.
7. **Recovery**: re-enable AWS east, monitor warm-up.
8. **Postmortem**: write `docs/GAMEDAY-03.md` with timeline, actions,
   action items.

### Demo script (the one you'd actually give to a CIO)

1. **0:00** — Single Cloudflare DNS. Show the global routing map.
2. **1:00** — Single Grafana pane: three clouds, one screen.
3. **2:00** — Click into a sovereign tenant request. Show the audit trail
   that it never left EU.
4. **3:00** — Trigger the AWS us-east-1 kill (or just show the recording
   from the game day).
5. **5:00** — Show the capacity scheduler placing a job on OCI because
   AWS H100 was unavailable.
6. **7:00** — FinOps: show ratio of multi-cloud opex to single-cloud
   baseline (target ≤ 1.20×).
7. **9:00** — Q&A.

### Final deliverable artifact

- 12-slide deck summarizing the architecture
- 5-minute screen recording of the demo
- 12+ ADRs in `src/adrs/`
- FY1 cost projection in `docs/COST-MODEL.md`
- Runbooks in `docs/DEPLOYMENT.md` and `docs/INCIDENT-MULTICLOUD.md`

---

## Stretch Goals

If you finish early:

- **Megaport NaaS** in place of IPsec for cross-cloud connectivity. Measure
  jitter improvement on east-west mTLS.
- **Cilium ClusterMesh** alongside Istio multi-primary, compare CPU
  overhead at 1k req/s.
- **Karmada or Open Cluster Management** for multi-cluster app deployment
  beyond Argo CD's app-of-apps.
- **GAIA-X catalog** integration evaluation for an alternative EU
  sovereign cell (OVHcloud or T-Systems).
- **Right-sized commitment portfolio**: write a small optimizer that
  proposes 1-year reservations across all four clouds based on the
  steady-state usage in your FinOps table.
- **DLP at egress**: hook AWS Macie + GCP DLP into cross-cloud transfers
  and demonstrate a policy block on PII data.
- **Confidential GPU**: experiment with NVIDIA H100 Confidential Compute
  mode in Azure CC and measure perf hit.

---

## Common Failure Modes During Build (cross-phase)

These bite repeatedly; bookmark this section.

### Identity & federation

- "I federated SPIRE but workloads still fail mTLS" — they're using the
  cluster default CA, not the SPIRE-issued cert. Wire your sidecar /
  application to load `/run/spire/svid/*` explicitly.
- "WIF works for `tofu plan` but not `apply`" — the GCP SA can read but
  not write; you bound `viewer` instead of the role you need.

### Networking

- Cross-cloud connectivity test passes with `ping` but fails on HTTPS —
  almost always asymmetric routing or MSS clamping; you accept SYN over
  one tunnel and try ACK over another. Force-prefer one tunnel.
- "Cross-AZ traffic is killing my bill" — you forgot
  `topologySpreadConstraints` and pods land on the wrong AZ; or your
  Service has no topology hints.
- Cloudflare returns "no healthy origins" right after a deploy — your
  health check tightly checks a dependency that's still rolling. Loosen
  the dependency check or stagger deploys per region.

### Multi-cluster / mesh

- Istio east-west gateway shows "503 NR" — east-west gateway can't be
  reached; almost always a security group / firewall rule blocks
  `15443/tcp`.
- "Service exists in both clusters but only one is called" — locality
  load balancing is doing its job; remove the localityLbSetting to test
  cross-cluster.

### Data / catalog

- "Polaris table create fails with `Forbidden: KMS`" — the catalog
  service account has S3 perms but no KMS Decrypt on the artifact CMK.
- "Iceberg snapshot inconsistent across clouds" — replication is
  metadata-only; ensure data files are replicated by the underlying
  bucket replication before exposing the table.

### Cost

- The bill 3× in one week and you can't find why — 9 of 10 times it's
  NAT gateway egress from an accidental DNS leak to `s3.amazonaws.com`
  instead of the regional VPC endpoint.
- Egress charges from a cluster you forgot to destroy — `tofu state list
  | xargs tofu state show` to enumerate; build a teardown CI workflow
  that runs nightly on PRs labeled `lab`.

### Sovereignty

- "Sovereign tenant request hit a US Cloudflare POP" — geo-steering is
  set but a CDN cache miss fell back to default tier; configure
  geo-fenced cache and disable default tier failover for those routes.
- Vault released a key to the wrong workload — your attestation policy
  matches on container image but not on the right namespace + service
  account; add both.

---

## When you finish

- **Tear down EVERY cloud account** with `tofu destroy` and verify in each
  console. Multi-cloud teardown takes longer than single-cloud; budget
  half a day.
- Verify your $300 alarms never fired.
- Archive the repo, deck, recording, and the three `GAMEDAY-*.md` files.
- Write a one-page reflection: which **architectural choices changed**
  during the build vs. the design doc, and **why**. Multi-cloud almost
  always changes plans during build; that's where you learn the most.

**You have now shipped, in miniature, the same multi-cloud topology a
Fortune 500 cloud architect runs in production — including the boring,
load-bearing parts (federated identity, cross-cloud catalog, FinOps,
sovereignty) that most "multi-cloud" decks gloss over.**
