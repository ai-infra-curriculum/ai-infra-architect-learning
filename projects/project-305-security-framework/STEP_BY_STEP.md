# Security & Compliance Framework — Step-by-Step Build Guide

> Project 305 | 70 hours total, organized as a 9-week part-time build
> Companion to `architecture.md`. Read that first.

This guide walks a learner from an empty AWS account to a working,
opinionated security framework: zero static credentials, supply-chain
provenance with Sigstore + SLSA-3, runtime detection with Falco +
Tetragon, OPA + Kyverno admission, Vault for secrets, a small audit
lake feeding Wazuh SIEM, evidence collection for SOC 2 controls, and
a purple-team drill that proves the controls work. Lab spend target:
**≤ $400** over 9 weeks with nightly teardown.

---

## Pre-Requisites Checklist

Before week 1:

- [ ] AWS account with admin or near-admin (a sub-account in an Org is
      ideal). A second account (or sub-account) for the **attacker**
      simulation is useful but optional.
- [ ] Budget alarms at $50, $150, $300.
- [ ] **CLI tooling** installed (pinned versions):
  - `aws` 2.15+
  - `kubectl` 1.30
  - `helm` 3.14+
  - `tofu` 1.6+ or `terraform` 1.7+
  - `cosign` 2.x
  - `syft` 1.10+
  - `trivy` 0.50+
  - `grype` 0.79+
  - `gitleaks` 8.18+
  - `semgrep` 1.70+
  - `vault` 1.16+
  - `spire-server` / `spire-agent` 1.9+
  - `falco` 0.38+ (charts only, runs as DaemonSet)
  - `tetragon` 1.1+ CLI
  - `argocd` 2.11+
  - `opa` 0.65+ + `gatekeeper` 3.16+ + `kyverno` 1.12+
  - `wazuh` (server runs in cluster)
  - `tines` (free dev tier, optional) or use GH Actions for SOAR
  - `jq`, `yq`, `gh`, `pre-commit`
- [ ] **Github org** with at least three private repos:
  `security-policy`, `security-runbooks`, `secure-by-default-template`.
- [ ] **Okta developer org** (free) or Keycloak in Docker.
- [ ] You are comfortable reading K8s YAML, Rego, and basic Go/Python.

### Recommended reading before starting

- *Container Security*, Liz Rice (O'Reilly) — fundamentals.
- *Zero Trust Networks*, Gilman & Barth.
- SLSA spec (v1.0).
- OPA + Gatekeeper docs.
- SPIFFE / SPIRE concepts.
- OWASP LLM Top 10 (2024).
- Sigstore concepts + Cosign keyless.
- The full `architecture.md` for this project.

### Cost ceiling for the lab build

| Phase | Approx. spend if torn down nightly | Notes |
|-------|------------------------------------|-------|
| 1 | $40 | EKS + IAM + KMS + Vault dev |
| 2 | $60 | Sigstore + Buildkite-style runner + admission |
| 3 | $80 | Falco + Tetragon + SIEM (Wazuh small) |
| 4 | $60 | Network policies + egress + Vault upgrade |
| 5 | $60 | OPA/Kyverno + tagging + IAM scans |
| 6 | $60 | LLM guardrails + tool-use gates |
| 7 | $40 | Purple-team drill + evidence pack |
| **Total** | **~$400** | $300 alarm should never fire |

---

## Phase 1 — Foundations (Week 1, ~7 hrs)

### Phase 1 goals

- EKS cluster, Vault dev, OIDC federation to AWS, three security repos
  scaffolded.
- A "secure-by-default" repo template.

### Day 1 — Cluster + Vault (3 hr)

1. Terraform `envs/sec-lab`: VPC, EKS 1.30 (re-use 301's cluster if you
   have it), KMS CMK.
2. Helm install Vault in dev mode (lab only). Configure KV path
   `secret/sec-lab/*`.
3. Install External Secrets Operator.

### Day 2 — OIDC federation to AWS (2 hr)

1. Create an AWS IAM OIDC provider for
   `token.actions.githubusercontent.com`.
2. Three roles: `gh-sec-lab-readonly`, `gh-sec-lab-plan`,
   `gh-sec-lab-apply`. Trust on
   `repo:org/security-policy:environment:lab`.
3. Verify with a tiny workflow that does `aws sts get-caller-identity`.
4. **Sweep the account for static keys**; rotate any you find;
   document a process to keep static keys at zero.

### Day 3 — `security-policy` repo + Conftest (2 hr)

1. Repo layout:
   ```
   rego/
     k8s/
       require_labels.rego
       no_root.rego
       image_allowlist.rego
     terraform/
       no_public_buckets.rego
       required_tags.rego
   policies/    # bundle manifests
   tests/       # opa test fixtures
   ```
2. Write one terraform policy (required tags) and one K8s policy
   (image allowlist). Add `opa test` to CI.
3. Add Conftest workflow: on PRs in `*-infra` repos, runs
   `conftest test` against `tofu plan -json`.
4. Verify a deliberately-bad PR is blocked.

### Phase 1 deliverables

- [ ] EKS + Vault dev running
- [ ] OIDC federation to AWS; no static keys
- [ ] `security-policy` repo with passing `opa test` CI
- [ ] Conftest CI in at least one repo blocks a bad PR

### Phase 1 failure modes

- OIDC role assume fails with "sub mismatch" — environment name
  doesn't match exactly (case-sensitive).
- Vault dev mode wipes secrets on restart — that's by design; for the
  lab it's fine, just re-seed.
- Conftest passes when it shouldn't — your test fixtures don't cover
  the negative case; add deny tests.

---

## Phase 2 — Supply Chain SLSA-3 (Week 2, ~10 hrs)

### Phase 2 goals

- A reference image built hermetically with SBOM + signature +
  provenance.
- Admission verification in the cluster.

### Day 1 — Hermetic-ish build (3 hr)

1. A demo Go service repo `demo-svc`.
2. GitHub Actions workflow:
   - Pin to a specific runner OS version + tools.
   - Use Kaniko (or Buildkit with explicit cache).
   - Build with `--reproducible` flags.
3. Push to ECR with image digest stamped to the workflow summary.

### Day 2 — SBOM + Cosign signing (3 hr)

1. Generate SBOM with Syft (`syft <image> -o spdx-json`); attach
   to image via `cosign attach sbom`.
2. Sign keyless with Cosign:
   ```
   cosign sign --identity-token <gh-oidc-token> <image-digest>
   ```
3. Generate SLSA-3 provenance with `slsa-github-generator`. Attach via
   `cosign attest`.
4. Confirm in Rekor's transparency log.

### Day 3 — Admission verification (2 hr)

1. Install Sigstore `policy-controller` in the cluster.
2. ClusterImagePolicy: require signature by the GitHub workflow
   identity for the `demo-svc` repo only.
3. Attempt to deploy:
   - The signed image: allowed.
   - An unsigned image: blocked, clear error.

### Day 4 — Vulnerability + secret + SAST gates (2 hr)

1. Trivy scan in the workflow; fail on HIGH+CRITICAL CVE counts above
   threshold (with exception annotation path).
2. Gitleaks on PRs.
3. Semgrep with a curated ruleset on PRs.
4. Verify a PR introducing a fake AWS key is blocked.

### Phase 2 deliverables

- [ ] `demo-svc` image signed (Cosign keyless) with provenance + SBOM
- [ ] Rekor entry visible
- [ ] Policy-controller blocks unsigned images
- [ ] CI gates: CVE, secret-scan, SAST

### Phase 2 failure modes

- Cosign sign fails "no OIDC issuer" — you didn't run inside a
  GitHub Actions environment, or the workflow lacks
  `permissions: id-token: write`.
- Policy-controller doesn't enforce — webhook namespace selector
  excludes your namespace; double-check.
- Trivy false positives flood the CI — pin a known-good ignore list
  and review monthly.

---

## Phase 3 — Runtime Security (Week 3, ~10 hrs)

### Phase 3 goals

- Falco + Tetragon detecting attacker behaviors.
- Wazuh SIEM ingesting events.
- One SOAR runbook auto-isolating a compromised pod.

### Day 1 — Falco (3 hr)

1. Helm install `falcosecurity/falco`. eBPF driver (modern path).
2. Enable `falcosidekick` to forward events to a webhook + S3.
3. Trigger a known rule: `kubectl exec` into a pod and run `cat /etc/shadow`. Falco fires.

### Day 2 — Tetragon (2 hr)

1. Install Tetragon (`isovalent/tetragon`).
2. Apply a `TracingPolicy` for "process spawning shell in a non-shell
   container" + "network connection from training pods to non-
   whitelisted IPs".
3. Trigger a deliberate violation; observe the event with full
   process tree context.

### Day 3 — Wazuh SIEM (3 hr)

1. Helm install Wazuh server + indexer (small-sizing for lab).
2. Configure Falco + Tetragon to forward to Wazuh via the Wazuh agent
   on each node (or directly via the API).
3. Build a dashboard: detections by rule, by namespace, last 24 h.

### Day 4 — Audit lake (1 hr)

1. S3 bucket `sec-lab-audit-${ACCT}` with Object Lock in **governance
   mode** (lab; compliance for prod). 7-year retention rule (overkill
   for lab — set 30 days).
2. Kinesis Firehose ingest: Falco + Tetragon events partitioned by
   day.
3. Glue + Athena: query the lake.

### Day 5 — First SOAR runbook (1 hr)

1. GitHub Actions workflow `runbook-isolate-pod.yml`:
   - Input: namespace, pod name.
   - Apply a deny-all NetworkPolicy targeted at that pod via label.
   - Kill the pod.
   - Capture node logs + Falco context to S3.
2. Trigger from a Wazuh alert via webhook (use the wazuh `integratord`).
3. Validate end-to-end: synthetic alert → runbook executes → pod
   isolated within 60 s.

### Phase 3 deliverables

- [ ] Falco + Tetragon running on every node
- [ ] Wazuh ingesting and showing events
- [ ] Audit lake populated with structured events
- [ ] One SOAR runbook end-to-end functional

### Phase 3 failure modes

- Falco eBPF driver doesn't load — kernel mismatch; check the
  `--modern-bpf` flag and Falco's compatibility matrix.
- Tetragon overwhelms Loki / SIEM with events — apply a coarser
  filter; tetragon can be too chatty.
- Wazuh runs but UI returns 500 — Indexer is OOM; size for at least
  4 GiB.

---

## Phase 4 — Zero-Trust Network + Vault (Week 4, ~8 hrs)

### Phase 4 goals

- Cilium L7 + FQDN policies enforced.
- Egress proxy with allowlist.
- Vault graduated from dev to "real-ish" with dynamic DB secrets.

### Day 1 — Cilium with deny-by-default (2 hr)

1. Install Cilium (or enable EKS Cilium add-on) with network policy
   mode.
2. Apply default-deny `CiliumNetworkPolicy` in `tenant-*` namespaces.
3. Allowlist intra-namespace + DNS only by default.

### Day 2 — Egress proxy + DNS-based allowlist (3 hr)

1. Helm install a Squid (or use Cilium FQDN policies natively).
2. Allowlist: `*.amazonaws.com`, the OIDC issuer, ECR, your registry.
3. Block everything else; spot-check by trying to curl `example.com`
   from inside a pod (denied).

### Day 3 — Vault dynamic DB secrets (3 hr)

1. Move Vault from dev to file-storage (lab) with shamir unseal keys
   stored separately.
2. Enable the database secrets engine for a small Postgres in your
   account.
3. A workload pulls a temporary (15-min TTL) user/password via Vault
   Agent injector or CSI provider.
4. Verify the credentials expire on schedule and Vault revokes
   server-side.

### Phase 4 deliverables

- [ ] Cilium default-deny in tenant namespaces
- [ ] Egress proxy with allowlist, denials logged to audit lake
- [ ] Vault issuing dynamic DB credentials with TTL ≤ 15 min
- [ ] Documented procedure for an emergency Vault unseal

### Phase 4 failure modes

- Default-deny breaks platform pods — your platform pods are in
  tenant-style namespaces; either add explicit allow policies or
  move them out.
- Egress allowlist over-blocks (npm install, pip install fails) —
  add the mirror domains explicitly.
- Vault DB engine rotation breaks long-running queries — set the
  lease longer for that workload's role.

---

## Phase 5 — OPA / Kyverno + Cross-Cutting Policy (Week 5, ~8 hrs)

### Phase 5 goals

- Hard-enforced admission policies cluster-wide.
- A "secure-by-default" Backstage template (or just a cookiecutter)
  that gives developers compliant defaults out of the box.

### Day 1 — Gatekeeper + Kyverno (3 hr)

1. Install both. Reasonable, simple set:
   - **Gatekeeper**: required labels, image registries, pod security.
   - **Kyverno**: auto-inject required labels, default-deny network
     policy on new namespaces, deny `privileged` pods.
2. Validate by trying to deploy a non-compliant pod; should be
   denied with a clear reason.

### Day 2 — Pod Security Standards (1 hr)

1. Apply `restricted` PSS to all tenant namespaces via Kyverno or
   built-in PodSecurity admission.

### Day 3 — Secure-by-default scaffolder (3 hr)

1. A cookiecutter (or Backstage template) that scaffolds:
   - GitHub repo with branch protection + CODEOWNERS preconfigured.
   - GH Actions wired to OIDC for AWS.
   - Pre-merge gates: CodeQL/Semgrep/Gitleaks/Conftest.
   - Container build with hermetic flags, Cosign signing, SBOM, SLSA.
   - K8s manifests with `restricted` PSS, default-deny network policy,
     required labels, ServiceAccount + IRSA-bound IAM role.
2. Generate one new project from the template and deploy it.

### Day 4 — IAM scanning + drift detection (1 hr)

1. Daily Lambda or GitHub Actions cron that:
   - Lists IAM users; flags any with active access keys.
   - Lists roles with overly-broad trust policies (e.g., `Principal: *`
     without conditions).
   - Posts findings to a Slack channel + ticket.

### Phase 5 deliverables

- [ ] Cluster-wide admission policies blocking common misconfigurations
- [ ] `restricted` PSS enforced in tenant namespaces
- [ ] Scaffolder produces a secure-by-default project in one command
- [ ] IAM scanner running daily

### Phase 5 failure modes

- Gatekeeper + Kyverno duplicate denies → noisy logs — pick one
  enforcer per policy class.
- PSS `restricted` breaks existing pods — migrate per namespace; use
  `audit` mode first to find offenders.
- Scaffolder template drifts from the latest framework — version the
  template and regenerate-bot weekly.

---

## Phase 6 — AI-Specific Controls (Week 6, ~10 hrs)

### Phase 6 goals

- LLM guardrails + prompt-injection defenses + tool-use gating.
- A safety-eval pipeline producing weekly scorecards.

### Day 1 — Llama Guard 3 + NeMo Guardrails (3 hr)

1. If you have project 303's LLM platform: re-use it. Otherwise stand
   up a tiny vLLM + a stub orchestrator.
2. Deploy Llama Guard 3 as input + output guard.
3. Configure NeMo Guardrails 0.10 with a policy file per tenant.

### Day 2 — Prompt-injection battery (3 hr)

1. 20 attacks based on OWASP LLM01:
   - Direct override ("ignore previous instructions")
   - Indirect (planted in retrieved chunk)
   - Tool misuse (try to coax the model into calling a `write` tool
     without confirmation)
   - Exfil-shaped (trick the model into emitting secret)
2. Score block rate; document failures; tune guardrails.

### Day 3 — Tool-use gating (2 hr)

1. MCP-style tool registry. Each tool declares blast radius:
   `read`, `write`, `external-effect`.
2. Orchestrator: any tool above `read` requires explicit user
   confirmation in the chat UI.
3. Tool calls audited to the lake.

### Day 4 — Model risk classification (1 hr)

1. Registration form: every model registered with risk class
   (EU AI Act); high-risk requires MRM sign-off before promotion.
2. OPA policy enforces.

### Day 5 — Honey-tokens + LLM data egress monitoring (1 hr)

1. Plant a fake credential string in your RAG corpus; if any response
   ever contains it, fire P1.
2. Pipe LLM gateway events through the egress audit lake with PII
   redaction.

### Phase 6 deliverables

- [ ] Guardrails inline (input + output)
- [ ] Prompt-injection battery scored; ≥ 18/20 blocked
- [ ] Tool-use gating with default human-in-the-loop above `read`
- [ ] Model risk classification gate
- [ ] Honey-token tripwire in RAG

### Phase 6 failure modes

- Llama Guard 3 false-positives benign content — tune threshold per
  safety category; do not just trust the final label.
- Tool-confirmation UI gets bypassed by an agent loop — enforce in the
  orchestrator backend, not just UI.
- Honey-token never gets retrieved (so it's not really a tripwire) —
  ensure it's indexed and accessible to retrieval.

---

## Phase 7 — Evidence, GRC, Purple Team, Demo (Weeks 7–9, ~17 hrs)

### Day 1–2 — Evidence collector (4 hr)

1. Service `evidence-collector-svc`:
   - Daily snapshots of: OPA policies, Vault config, IAM grants
     (sanitized), image registry inventory, model registry, network
     policies, KMS key rotation status, Lake Formation grants (if
     you have 304).
   - Land in audit lake as structured JSON with a stable schema.
2. Daily Merkle digest job hashes prior day's partitions; writes the
   digest to a separate WORM bucket.

### Day 3 — GRC tool integration (3 hr)

1. Drata / Vanta / Hyperproof — pick one (free trial for the lab).
2. Map controls:
   - SOC 2 CC6 (logical access) → Vault config + IAM scanner output.
   - SOC 2 CC7 (system operations) → Falco + audit lake.
   - SOC 2 CC8 (change management) → branch protection + CODEOWNERS.
   - ISO 27001 A.5–A.8 — pick at least 10 controls.
   - EU AI Act high-risk — model card schema + risk register.
3. Validate evidence flows automatically.

### Day 4 — Auditor view (2 hr)

1. Backstage (or just a static site) page with scoped read-only
   evidence access per control. Audit a sample with a friend acting
   as auditor; capture friction.

### Day 5 — Purple-team drill (4 hr)

Sequenced attack chain:

1. **Initial access**: pretend an attacker compromises a CI runner
   (you simulate by leaking a short-TTL OIDC token).
2. **Persistence**: try to extend access via a workload's SVID; the
   attempt should fail thanks to short TTLs.
3. **Lateral movement**: from a pod in `tenant-a`, try to reach the
   audit lake or another tenant. Cilium policy + Vault scoping should
   block.
4. **Privilege escalation**: try to spawn a privileged container.
   PSS + Gatekeeper blocks.
5. **Exfiltration**: try a curl to a non-allowlisted external IP.
   Egress proxy blocks; alert fires.
6. **Honey-cred touched**: as you poke around, you intentionally
   touch the planted fake AWS keys; P1 fires within 1 minute.

Document each step: detection time, containment time, post-action
debrief.

### Day 6 — KPI dashboards (2 hr)

1. Grafana dashboards:
   - MTTD trend.
   - MTTC trend.
   - Number of policy violations per cluster per week.
   - Image admission denial rate.
   - LLM guardrail block rate per tenant.
2. SLO panel: % of detections within target.

### Day 7 — Demo & write-up (2 hr)

Demo script (the one for the CISO):

1. **0:00** — Live: deploy an unsigned image. Blocked at admission.
2. **1:30** — Live: try to deploy a privileged pod. PSS blocks.
3. **3:00** — Live: trigger a Falco rule from inside a pod. SOAR
   isolates the pod in ≤ 60 s.
4. **4:30** — Walk through the purple-team report. Show ATT&CK
   coverage matrix.
5. **6:30** — Open the GRC tool: SOC 2 CC6/CC7/CC8 evidence flowing
   automatically. Pick a random control and show the source data.
6. **8:00** — LLM bot demo: 20-attack battery; show block rate; show
   the tool-use confirmation in action.
7. **9:30** — Q&A.

### Phase 7 deliverables

- [ ] Evidence collector + Merkle digest live
- [ ] GRC tool ingesting evidence for ≥ 10 controls
- [ ] Auditor view validated by a friendly auditor
- [ ] Purple-team drill report with detection + containment times
- [ ] Security KPI dashboards
- [ ] Demo recorded (≤ 5 min)
- [ ] 12+ ADRs in `src/adrs/`

---

## Stretch Goals

- **Cedar at the application layer**: pick one app, migrate authz from
  ad-hoc code to Cedar; compare reviewability vs. Rego.
- **Confidential compute**: stand up an Azure Confidential Containers
  workload with attestation-gated Vault unwrap (re-uses 302 phase 4).
- **UEBA-lite**: build a small ML scorer on Wazuh events
  (anomalous-actor detection by hour/role pair).
- **OpenSearch SIEM** as an alternative to Wazuh; compare cost +
  detection authoring.
- **Threat-model automation**: a tiny tool that ingests a service's
  README + arch diagram and emits a STRIDE-style first draft for
  human review.
- **Continuous evidence verification**: cryptographic proof every
  evidence pack is unmodified end-to-end (transparency log style).
- **Sovereign cell drill**: extend the framework to the EU sovereign
  cell from 302; demonstrate trust-domain separation under attack.
- **Tabletop game**: write a multi-round tabletop scenario card deck
  and run it with the SOC.
- **MITRE ATLAS coverage** for AI-specific threats; cross-walk with
  the existing ATT&CK coverage.

---

## Common Failure Modes During Build (cross-phase)

### Identity

- "Static keys keep reappearing" — someone's onboarding flow still
  generates them; fix the flow at source, then sweep again.
- "SVID rotation breaks long-running jobs" — increase TTL specifically
  for known-batch workloads; do not weaken the default.

### Policy

- "OPA bundles serve stale policy" — your bundle service caches; set
  `discovery.decision.cache-ttl-seconds` low (e.g., 30).
- "Kyverno mutates without authority" — order matters; mutating
  policies must precede validating ones in admission chain.

### Supply chain

- Cosign verification fails for legitimate images — your trusted
  identity list missed the actual OIDC subject; check
  `cosign verify --certificate-identity`.
- Provenance not generated — the `slsa-github-generator` workflow
  ran on a fork without `id-token: write`; fix permissions.

### Runtime

- Falco rules too noisy in tenant namespaces — annotate noisy rules
  with `exception` patterns per namespace.
- Tetragon misses kernel events under high pod density — confirm
  the Tetragon Agent is using a kernel ≥ 5.10 with full eBPF
  features.

### Network

- "DNS works but TCP doesn't" — likely SG / network policy on egress.
- Egress proxy logs blank — the proxy is bypassed because the pod
  has direct internet via NAT gateway; fix at VPC route tables.

### Detection / response

- Wazuh dashboards lag — Indexer is undersized for the event volume;
  rate-limit Falco/Tetragon or grow Wazuh.
- SOAR runbook fails mid-execution — runbooks must be idempotent;
  rerun and verify nothing is double-applied.

### LLM / AI

- Guardrails block legitimate finance content — domain-specific
  exceptions in NeMo Guardrails; revisit per quarter.
- Tool gating is bypassable via tool-chains the orchestrator doesn't
  see — instrument every tool call site in the orchestrator code, not
  just at the framework boundary.

### GRC / evidence

- Auto-evidence misses a control because no system emits it — manual
  attestation path with proof-of-process artifacts (screenshot,
  document) attached to the control.
- Evidence pack grows huge — keep snapshots small + diff-based; full
  state daily, incremental hourly.

---

## When you finish

- Tear down ALL resources: EKS, Vault, Wazuh, ElastiCache, S3 (after
  emptying — note that audit-lake with Object Lock in compliance mode
  is irreversible; use governance mode in the lab to allow teardown).
- Confirm the $300 alarm never fired.
- Archive: repo, recording, drill report, evidence-pack sample.
- Write a one-page reflection: which **assumption you had at design
  time** changed during the build, and what that implies for how you'd
  architect the framework next time.

**You have now shipped, in miniature, the same security controls a
Fortune 500 security team operates at production scale — including
the boring, load-bearing parts (zero static keys, supply chain
provenance, audit-lake-as-evidence) that most "security architecture"
decks gloss over.**
