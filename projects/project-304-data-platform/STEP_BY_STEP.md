# Data Platform for AI — Step-by-Step Build Guide

> Project 304 | 85 hours total, organized as a 10-week part-time build
> Companion to `architecture.md`. Read that first.

This guide walks a learner from an empty AWS account to a working
lakehouse: Iceberg + Polaris, an ingestion pipeline from at least three
source types (CDC, SaaS, batch), dbt-modeled Silver and Gold layers, a
metric layer, OpenLineage end-to-end, Great Expectations quality suites,
data contracts with CI enforcement, lineage in DataHub, and a small AI
workload consumption demo. Lab target spend: **≤ $500** over 10 weeks
with nightly teardown.

---

## Pre-Requisites Checklist

Before week 1:

- [ ] AWS account with admin or near-admin (sub-account in an
      Organization ideal).
- [ ] Budget alarms at $50, $150, $300.
- [ ] A source database to do CDC against. Easiest: spin up a Postgres
      RDS in your account with the `pagila` sample dataset.
- [ ] A SaaS source. Easiest: a free Stripe or Salesforce developer
      account (sandbox). Lazy substitute: dump a CSV into S3 on a
      schedule.
- [ ] **Tools installed** (pinned versions):
  - `aws` 2.15+
  - `kubectl` 1.30
  - `helm` 3.14+
  - `tofu` 1.6+ or `terraform` 1.7+
  - `dbt-core` 1.8 with `dbt-trino` and `dbt-spark[PyHive]`
  - `dbt-iceberg` adapter (community)
  - `spark-submit` 3.5
  - `trino` 450 CLI
  - `flink` 1.19 CLI
  - `argo` 3.5 CLI
  - `marquez` 0.45+
  - `great_expectations` 0.18+
  - `soda-core` 3.3+
  - `datahub` 0.13+ CLI
  - Python 3.12, Java 11/17 for Spark/Flink/Trino
  - `jq`, `yq`, `gh`, `duckdb`
- [ ] An IDE comfortable with both Python and SQL (VS Code + dbt
      extension is fine).
- [ ] Familiarity with: SQL (window functions especially), Spark basics,
      Avro/Parquet, basic Kafka concepts.

### Recommended reading before starting

- *Building the Data Lakehouse*, Inmon / Levins / Jain
- Iceberg spec — read sections on snapshots and partitioning
- dbt "Best practices" guide; "Metric layer" docs
- OpenLineage spec — events, datasets, jobs
- Open Data Contract Standard (ODCS) repo README
- The full `architecture.md` for this project

### Cost ceiling for the lab build

| Phase | Approx. spend if torn down nightly | Notes |
|-------|------------------------------------|-------|
| 1 | $40 | EKS + S3 + KMS + Polaris |
| 2 | $80 | MSK Serverless small + RDS for CDC |
| 3 | $80 | Spark on EKS + first ingest |
| 4 | $90 | dbt + Trino + lineage |
| 5 | $80 | DQ + contracts + DataHub |
| 6 | $60 | Feast + AI consumer demo |
| 7 | $70 | Streaming + DR drill |
| **Total** | **~$500** | $300 alarm should never fire |

---

## Phase 1 — Foundation (Week 1, ~7 hrs)

### Phase 1 goals

- EKS cluster, S3 buckets (one per layer), KMS, ECR, IAM with Lake
  Formation Admin role.
- Polaris catalog deployed.

### Day 1 — VPC + EKS + S3 (3 hr)

1. Terraform `envs/lab-dp`: VPC, EKS 1.30, ECR, KMS CMK.
2. S3 buckets: `dp-lab-bronze-${ACCT}`, `-silver-`, `-gold-`,
   `-audit-`, `-metastore-`. All KMS-encrypted with the CMK, lifecycle
   to IA at 90d for bronze.
3. Lake Formation: set yourself as a Data Lake Administrator.

### Day 2 — Polaris (3 hr)

1. Helm install `apache/polaris` (community chart) on EKS. Backing
   store: Aurora Serverless v2 (min 0.5, max 2 ACU).
2. Create a service principal for the platform; mint client credentials
   into Vault.
3. Create the first namespace structure:
   ```
   tc/
     bronze/
     silver/
     gold/
     sandbox/
   ```
4. Smoke test with the `pyiceberg` library: create a table, write some
   data, list snapshots.

### Day 3 — Lineage backend (Marquez) (1 hr)

1. Helm install Marquez with its Postgres.
2. Verify the UI loads at `marquez.platform.lab`.
3. Smoke test by POSTing a dummy OpenLineage event with curl.

### Phase 1 deliverables

- [ ] EKS + S3 layered buckets + KMS done
- [ ] Polaris catalog running with `tc` namespace
- [ ] First Iceberg table created and queried with `pyiceberg`
- [ ] Marquez UI reachable, accepting events

### Phase 1 failure modes

- `pyiceberg` write fails with "no such namespace" — you authenticated
  to Polaris with a token that has no namespace privileges; grant the
  service principal `manage_grants` on `tc`.
- Polaris pod CrashLoopBackoff with DB connection errors — Aurora is
  serverless and may take 90 s to wake from pause; set Polaris
  `connectionTimeout` ≥ 120 s.

---

## Phase 2 — Ingestion (Weeks 2–3, ~12 hrs)

### Phase 2 goals

- CDC pipeline (Debezium → Kafka → S3 Bronze as Iceberg).
- Batch / file drop pipeline.
- Streaming application events.

### Day 1 — MSK + Schema Registry (3 hr)

1. MSK Serverless cluster (cheap for the lab).
2. AWS Glue Schema Registry for Avro schemas.
3. Postgres RDS with `pagila` data and `wal_level=logical`.

### Day 2 — Debezium → Kafka (3 hr)

1. Helm install Strimzi (operator) + a Kafka Connect cluster.
2. Deploy a Debezium PostgreSQL connector for `pagila`. Topic prefix
   `tc.bronze.pagila`.
3. Register Avro schemas in Glue Schema Registry with compatibility
   `BACKWARD`.
4. Verify changes flow: insert a row in `pagila.customer` and see it
   in the topic via `kcat`.

### Day 3 — Kafka → Iceberg Bronze (3 hr)

1. Two options:
   - **Recommended for lab**: Apache **Iceberg Kafka Connect Sink**
     (`tabular-io/iceberg-kafka-connect`). Writes directly to
     Iceberg tables in Polaris.
   - **Alternative**: Flink 1.19 with the Iceberg sink. Lower-level but
     more flexible.
2. Configure the sink to write `tc.bronze.pagila.public.customer` etc.
   partitioned by ingestion date.
3. Add the Bronze table as a Marquez dataset by configuring the sink's
   OpenLineage emitter.

### Day 4 — Batch file drop ingestion (2 hr)

1. A small Python script as a Kubernetes CronJob (or Airflow task)
   that:
   - Polls an SFTP-like S3 staging prefix.
   - Validates against a schema (`fastavro` or `pyarrow`).
   - Writes to `tc.bronze.partner_sales` as an Iceberg table.
2. Add OpenLineage emission via the `openlineage-python` client.

### Day 5 — Application events stream (1 hr)

1. Generate synthetic application events with a tiny `producer.py` that
   sends 100 events/s to topic `tc.events.clickstream`.
2. Iceberg Sink writes them to `tc.bronze.clickstream`.

### Phase 2 deliverables

- [ ] CDC: source DB changes appear in Bronze Iceberg within 1 minute
- [ ] Batch: a daily file lands as a new snapshot in `tc.bronze.partner_sales`
- [ ] Stream: clickstream events visible in Bronze
- [ ] OpenLineage events for each ingest job appear in Marquez

### Phase 2 failure modes

- Debezium snapshot takes hours on a small DB — your `snapshot.mode` is
  `always`; switch to `initial` and use `signaling` for re-snapshots.
- Iceberg sink commits fail with "table not found" — autoCreate=false by
  default; either pre-create or enable autoCreate with strict schema.
- `kcat` shows messages but the sink commits 0 records — the schema
  registry serializer mismatch; check that the sink's value converter
  matches Debezium's serializer.

---

## Phase 3 — Modeling (Weeks 3–4, ~12 hrs)

### Phase 3 goals

- dbt project structured Bronze → Silver → Gold for one domain.
- Spark for heavy work; dbt-trino for SQL transforms.
- First metrics defined in the semantic layer.

### Day 1 — Trino on EKS (2 hr)

1. Helm install `trinodb/trino` 450. Configure the Iceberg connector
   pointing to Polaris.
2. `trino> SHOW SCHEMAS FROM iceberg;` returns `bronze`, `silver`, etc.
3. Validate: `SELECT count(*) FROM iceberg.bronze.customer LIMIT 1;`

### Day 2 — Spark on EKS (2 hr)

1. Install Spark Operator. Build a Spark base image with the Iceberg
   runtime jar + Polaris REST catalog config.
2. Submit a job that compacts `tc.bronze.customer`. Verify snapshot
   count grows; `expire_snapshots` reduces.
3. Schedule a daily compaction via Airflow (or a CronJob).

### Day 3 — dbt project init (2 hr)

1. `dbt init dp_lab` with `dbt-trino` profile pointing at Trino.
2. Project structure:
   ```
   models/
     bronze/_sources.yml
     silver/customer/stg_customer.sql
     silver/customer/silver_customer.sql
     gold/customer/active_customers.sql
   tests/...
   semantic_models/...
   metrics/...
   ```
3. `dbt run --models silver.customer` materializes `silver.customer`
   as an Iceberg table.

### Day 4 — Silver modeling for one domain (3 hr)

1. Build `silver.customer`: dedupe by `customer_id` keeping latest by
   `updated_at`; type the columns; enforce non-null on key columns.
2. Build `silver.transactions`: join CDC + clickstream + partner
   batch into a unified shape.
3. Add `dbt test` rows: unique, not-null, accepted-values.

### Day 5 — Gold + Semantic Layer (3 hr)

1. Define `gold.dm_customer_activity` with daily aggregates.
2. Define a semantic model + metric `active_customers` using the dbt
   Semantic Layer (`MetricFlow`).
3. Use MetricFlow CLI to query the metric: `mf query --metrics
   active_customers --group-by metric_time__day`.

### Phase 3 deliverables

- [ ] Trino querying Iceberg via Polaris
- [ ] Daily compaction job for at least one Bronze table
- [ ] dbt Silver for `customer` domain with passing tests
- [ ] Gold mart + at least one metric defined in the semantic layer
- [ ] MetricFlow query returns expected numbers

### Phase 3 failure modes

- dbt `relation does not exist` when running models — the Trino catalog
  config in `~/.dbt/profiles.yml` is wrong (`catalog`, `schema`);
  align with the Polaris namespace path.
- Spark job kills itself with "Failed to commit to Iceberg" — concurrent
  commit conflict; enable Iceberg's commit retry settings
  (`commit.retry.num-retries: 4`).
- MetricFlow query returns weird counts — your time grain doesn't
  match the source partitioning; align.

---

## Phase 4 — Lineage & Discovery (Week 5, ~10 hrs)

### Phase 4 goals

- OpenLineage emitted from Spark, dbt, Airflow, Trino.
- DataHub up and ingesting catalog + lineage.
- A complete lineage graph from source to a gold metric.

### Day 1 — OpenLineage adapters (3 hr)

1. **Spark**: add the OpenLineage Spark integration jar; config in
   spark-defaults.
2. **dbt**: install `dbt-ol`; wrap `dbt run` calls.
3. **Airflow**: install `openlineage-airflow` provider; configure
   transport to Marquez.
4. **Trino**: install the OpenLineage event listener plugin.
5. Validate that every layer emits events: run a Spark compact, a dbt
   build, an Airflow DAG; confirm in Marquez UI.

### Day 2 — DataHub deploy (3 hr)

1. Helm install DataHub (`acryldata/datahub`). Backed by RDS Postgres
   + Elasticsearch (a small ES is fine in lab).
2. Configure ingestion recipes:
   - `polaris` ingestion (tables, namespaces).
   - `dbt` ingestion (manifest → DataHub).
   - `openlineage` push from Marquez to DataHub via the
     `marquez-to-datahub` bridge.

### Day 3 — Cataloging (2 hr)

1. Assign owners to every table in `tc.silver.customer.*`.
2. Add descriptions + business glossary terms.
3. Validate "Lineage" view: click on `gold.dm_customer_activity` and
   trace back to `bronze.customer`, `bronze.clickstream`, etc.

### Day 4 — Lineage SLO check (2 hr)

1. Build a small probe: for a random sample of Silver/Gold tables,
   verify they have lineage edges produced within the last 30 minutes.
2. Alert in Slack if coverage < 95%.

### Phase 4 deliverables

- [ ] Lineage events flowing from all four engines into Marquez
- [ ] DataHub showing the full lineage graph end-to-end
- [ ] Every table in `tc.silver` and `tc.gold` has a named owner
- [ ] Lineage coverage probe in place with Slack alert

### Phase 4 failure modes

- Spark job emits no OpenLineage events — the integration jar version
  doesn't match Spark version; pin compatible versions.
- DataHub ingestion silently drops tables — they have no
  `customProperties.platformInstance`; set it explicitly.
- Marquez → DataHub bridge duplicates lineage — set the URN namespace
  consistently across all emitters.

---

## Phase 5 — Quality, Contracts, Governance (Weeks 6–7, ~12 hrs)

### Phase 5 goals

- Data contracts on at least 3 producers; CI enforcement.
- Great Expectations + Soda suites on Silver/Gold tables.
- Column-level PII tagging and policy enforcement.

### Day 1 — Open Data Contract Standard (3 hr)

1. Create `data-contracts/` repo with ODCS YAML for one CDC, one batch,
   one streaming producer.
2. Define schema, SLAs (freshness, completeness), owner, version,
   quality rules.
3. Write a Python `contract-check` script:
   - Reads producer-side schema (DDL, Avro, JSON Schema).
   - Diffs against contract.
   - Classifies as compatible / non-breaking / breaking.
4. GitHub Actions workflow on producer-app PRs runs contract-check; a
   breaking change requires a `contract-bump` label + reviewer.

### Day 2 — Runtime contract enforcement (2 hr)

1. Bronze writes for the CDC pipeline: validate every payload against
   the registered Avro schema before commit; reject to DLQ.
2. Silver dbt builds: fail-fast on contract violations (column missing,
   type mismatch).

### Day 3 — Great Expectations + Soda (3 hr)

1. GX suite for `silver.customer`: 12 expectations covering schema,
   uniqueness, distribution, recency.
2. Soda Core checklist for `gold.dm_customer_activity`: thresholds on
   metric volatility.
3. Schedule via Airflow; results stored in GX's data docs (S3-hosted).

### Day 4 — Anomaly detection (2 hr)

1. A small Flink job consumes GX run results; computes 30-day moving
   averages and flags 3σ deltas; routes to PagerDuty for tier-1 tables.

### Day 5 — PII tagging + Lake Formation (2 hr)

1. Run AWS Macie on Bronze + Silver buckets; pull the findings.
2. A small tagger writes `pii=true` to Polaris column metadata for
   detected columns.
3. Lake Formation: configure column-level access for one Silver table
   (`pii_columns` group cannot SELECT those columns).
4. Validate: query as a user not in the group → those columns return
   redacted/null.

### Phase 5 deliverables

- [ ] 3 producers covered by ODCS contracts
- [ ] CI gate blocks a deliberate breaking change PR
- [ ] GX + Soda runs nightly; failures alert in Slack
- [ ] PII columns tagged and enforced via Lake Formation
- [ ] Anomaly detector firing on a deliberate volume drop

### Phase 5 failure modes

- Contract check passes on a breaking change — your diff function
  treats "column renamed" as "column dropped + new column"; add rename
  detection via column comments or migration metadata.
- GX `BatchRequest` fails on Iceberg — `great_expectations-iceberg`
  integration is young; fall back to running GX against a Trino
  connection.
- Lake Formation policy not applied — you forgot to register the table
  with Lake Formation; `aws lakeformation register-resource` first.

---

## Phase 6 — Serving for AI (Week 8, ~10 hrs)

### Phase 6 goals

- Feast offline reading Iceberg + online to Redis.
- A small ML feature pipeline consumed by a model.
- A LLM RAG corpus ingested through the lakehouse and exposed to
  project 303.

### Day 1 — Feast offline on Iceberg (3 hr)

1. Install Feast 0.39. Configure the Iceberg offline store (community
   plugin) pointing at Polaris.
2. Define a `FeatureView` over `silver.customer` (e.g., 30-day
   transaction count).
3. `feast apply` then `feast historical` against a few entities.

### Day 2 — Feast online on Redis (2 hr)

1. ElastiCache Redis 7 (`cache.t4g.small`).
2. `feast materialize` to push features to Redis.
3. Benchmark online get: p99 ≤ 10 ms target.

### Day 3 — Model uses governed features (2 hr)

1. Borrow 301's MLflow + a tabular pipeline. Train a model using the
   Feast feature view as input. Verify lineage edges from the model
   run back to the Iceberg source.

### Day 4 — Corpus for LLM RAG (3 hr)

1. Ingest a small document set (e.g., 500 Confluence-style docs) into
   `tc.bronze.docs` as an Iceberg table with `(doc_id, version, body,
   metadata)`.
2. Build a `tc.silver.docs_chunks` table via dbt + a small Spark UDF
   for chunking.
3. Expose the table to project 303's ingestion pipeline via Polaris
   read-only credentials.

### Phase 6 deliverables

- [ ] Feast offline + online live; online p99 ≤ 10 ms documented
- [ ] One model trained against Feast features with lineage back to
      source tables
- [ ] LLM RAG-consumable docs table published, with row-level
      provenance preserved

### Phase 6 failure modes

- Feast `online_write_batch` is slow — Redis cluster has the wrong
  shard layout; use `cluster-mode` only if you actually need it.
- ML model lineage missing — Feast's OpenLineage emitter is opt-in;
  enable it.
- LLM team queries the doc table and gets `permission denied` —
  Polaris read-only grant wasn't issued to their workload SVID; grant
  via SPIRE-mapped principal.

---

## Phase 7 — Streaming, DR, FinOps (Week 9, ~10 hrs)

### Phase 7 goals

- A real Flink streaming app updating a Gold aggregate.
- A DR drill that switches a tier-1 table to a secondary region.
- Per-team cost panel.

### Day 1 — Flink Gold aggregation (3 hr)

1. Flink job reads `tc.bronze.clickstream` (Kafka), windows 5-minute
   counts per `user_id`, writes to `tc.gold.realtime_user_activity`
   Iceberg table via the Iceberg Flink sink.
2. Validate by tailing the Iceberg table during a synthetic burst.

### Day 2 — DR drill (3 hr)

1. Set up S3 CRR to a secondary region for `tc.silver.customer` + its
   metadata bucket.
2. Stand up a secondary Polaris pointing at the secondary buckets.
3. Drill: pause writers, fail Trino over to the secondary catalog,
   query, validate row counts match.
4. Time the drill; target RTO ≤ 1 hour.

### Day 3 — Per-team cost panel (3 hr)

1. Tag every Spark/Trino/Flink job with `team`, `dataset`, `purpose`.
2. Collect Kubecost allocations + S3 storage size by prefix + Athena
   query bytes scanned per role.
3. ClickHouse + Grafana panel: $/team/day; flag top spenders.

### Day 4 — Query-waste budget proof of concept (1 hr)

1. Identify the top 10 most-expensive Trino queries last week.
2. For 3 of them, suggest optimizations (partition pruning, projection
   pushdown). Document the savings.

### Phase 7 deliverables

- [ ] Real-time Iceberg aggregation working
- [ ] DR drill executed with RTO ≤ 1 hour, RPO ≤ 15 min
- [ ] Per-team cost dashboard with at least 4 weeks of data
- [ ] Query-waste analysis document with concrete savings

### Phase 7 failure modes

- Flink → Iceberg sink commits every record (slow) — set
  `commit.interval` to ≥ 30 s with appropriate parallelism.
- DR failover succeeds but Polaris secondary has stale metadata —
  Polaris secondary was warm-replicated but not synced for the last
  N commits; replicate metadata more frequently (e.g., every commit).
- Kubecost shows $0 for Spark jobs — your Spark pods are missing the
  Kubecost labels; align labels.

---

## Phase 8 — Demo & Final Drills (Week 10, ~6 hrs)

### Final drill script (~2 hr)

1. **Regulator drill**: pick a metric value rendered in a BI tool
   yesterday. Trace it back to source tables through DataHub. Stopwatch:
   target ≤ 5 minutes.
2. **Schema-change drill**: open a PR adding a breaking schema change
   to one of your three contracted producers. Show CI blocking,
   downstream-impact comment posted, label-bump path.
3. **Erasure drill**: pick a customer ID; run a subject-erasure DAG;
   verify in 24 h the customer no longer appears in `silver.customer`,
   `gold.dm_customer_activity`, or Feast online store.
4. **AI consumption demo**: query the same metric from
   - Looker
   - Power BI (or a screenshot if you don't have it set up)
   - Project 303's LLM bot using text-to-SQL
   All three return identical numbers. Display side-by-side.

### Demo script (the one for a CDO)

1. **0:00** — DataHub home. Show "owner per table", lineage from a Gold
   mart back to sources.
2. **2:00** — Click a metric in dbt's semantic layer. Show that Looker,
   Power BI, and the LLM bot resolve to the same SQL.
3. **4:00** — Walk through the contract enforcement: a PR that breaks a
   schema, blocked.
4. **5:30** — Show the GX dashboards: pass rate per Silver table,
   anomaly hits last week.
5. **7:00** — Cost panel: spend per team, top wasted queries this week
   with proposed fixes.
6. **8:30** — DR drill recording (optional).
7. **9:30** — Q&A.

### Final deliverable artifact

- 12-slide deck
- 5-minute screen recording
- 12+ ADRs in `src/adrs/`
- `docs/COST-MODEL.md`, `docs/MIGRATION-PLAN.md`,
  `docs/GOVERNANCE.md`, `docs/DEPLOYMENT.md`
- Runbook `docs/INCIDENT-DATA.md`

---

## Stretch Goals

- **Snowflake → Iceberg coexistence**: register your Iceberg tables in a
  Snowflake account; run a workload that joins Iceberg + Snowflake-
  native tables.
- **Trino fault-tolerant execution**: enable for one heavy query and
  measure stability under simulated worker kills.
- **Unity Catalog OSS comparison**: stand up Unity Catalog beside
  Polaris and compare for one domain.
- **Spark Connect** for laptop dev experience that doesn't drag the
  cluster into IDE workflows.
- **DuckLake** pattern: build a signed-URL service that lets analysts
  query an Iceberg snapshot from DuckDB locally without burdening the
  shared Trino.
- **Iceberg V3 features**: deletion vectors, encryption keys at table
  level (when GA).
- **Federated identity for catalog**: SPIRE SVIDs for engines, no
  static catalog credentials.
- **Right-to-be-forgotten at scale**: implement the erasure framework
  with row-level deletes and tombstone compaction across all layers,
  scheduled monthly.
- **Cross-cloud catalog**: extend Polaris to span S3 + GCS + ADLS Gen2
  via 302's multi-cloud topology.

---

## Common Failure Modes During Build (cross-phase)

### Catalog & metadata

- "Iceberg snapshot expired but data files still in S3" — your
  `remove_orphan_files` cadence is too slow; run weekly minimum.
- "Polaris credential vending returns expired tokens" — clock skew on
  the engine nodes; ensure NTP is healthy.

### Ingest

- CDC lag spikes overnight — the source DB ran a large batch job;
  Debezium serializes through one WAL stream. Consider partitioning
  source tables or running a second connector for the hot table.
- File-drop ingestion produces duplicates — your idempotency key uses
  the filename only; switch to a content hash.

### Modeling

- dbt incremental builds re-process everything — your `is_incremental()`
  branch isn't being taken because the table doesn't exist on first
  run; safe to keep but make sure the predicate is index/sargable.
- A metric value drift after a Silver model change — you forgot to
  refresh downstream materializations; use dbt's `model_node`-based
  graph.

### Lineage

- DataHub lineage graph has "ghost" nodes — the same dataset URN was
  emitted with two different platform instances; normalize.
- OpenLineage events from Trino missing column-level lineage — the
  listener plugin's column-lineage feature must be enabled explicitly.

### Quality / contracts

- GX runs pass but downstream data is wrong — your expectations are
  schema-only; add distribution and reconciliation expectations.
- Contract diff false-positive — you compared schema text rather than
  semantic schema; use a schema-aware diff (`avro-tools`, JSON Schema
  diff).

### Cost

- S3 bill quadrupled — Iceberg's metadata file growth on a hot table;
  enable `snapshot.removal-strategy` and run compaction.
- Trino query bill explodes — a join order rewrite removed a filter
  pushdown; enable cost-based optimization stats.

### Performance

- Trino p95 query latency creeps up — too many small files per
  partition; daily compaction.
- Feast online write throughput drops — Redis maxmemory eviction is
  evicting hot keys; raise memory or use a dedicated keyspace.

---

## When you finish

- Tear down ALL resources: EKS, RDS, MSK, ElastiCache, S3 (after
  emptying), KMS (scheduled deletion). MSK + RDS are the silent costs.
- Verify your $300 alarm never fired.
- Archive: repo, deck, recording, runbook.
- Write a one-page reflection: how your **mental model of "data
  platform"** changed during the build. Almost everyone underestimates
  contracts and lineage on day 1; you'll see why.

**You have now shipped, in miniature, the same lakehouse + governance
control loops a Fortune 500 data platform team operates at production
scale — including contracts, lineage, and quality, the load-bearing
parts that demos usually skip.**
