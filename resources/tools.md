# AI Infrastructure Architect - Tools and Software

Comprehensive list of tools for AI infrastructure architecture work.

## Architecture Design Tools

### Diagramming and Modeling

1. **Draw.io (diagrams.net)**
   - **Type**: Free, open-source diagramming
   - **Use**: Architecture diagrams, flowcharts
   - **Link**: [draw.io](https://www.draw.io)
   - **Export**: PNG, SVG, PDF, XML
   - **Recommendation**: Best free option

2. **Lucidchart**
   - **Type**: Commercial ($7.95-$20/month)
   - **Use**: Professional diagramming, collaboration
   - **Link**: [lucidchart.com](https://www.lucidchart.com)
   - **Features**: Real-time collaboration, templates
   - **Recommendation**: For teams

3. **ArchiMate Tool (Archi)**
   - **Type**: Free, open-source
   - **Use**: Enterprise architecture modeling
   - **Link**: [archimatetool.com](https://www.archimatetool.com)
   - **Standard**: ArchiMate 3.1
   - **Recommendation**: For TOGAF practitioners

4. **PlantUML**
   - **Type**: Free, open-source
   - **Use**: Diagram as code
   - **Link**: [plantuml.com](https://plantuml.com)
   - **Format**: Text-based diagrams
   - **Recommendation**: For version control

5. **Mermaid**
   - **Type**: Free, open-source
   - **Use**: Diagrams in Markdown
   - **Link**: [mermaid.js.org](https://mermaid.js.org)
   - **Integration**: GitHub, GitLab, Notion
   - **Recommendation**: For documentation

### Enterprise Architecture Tools

6. **Sparx Enterprise Architect**
   - **Type**: Commercial
   - **Use**: Enterprise architecture, UML, BPMN
   - **Recommendation**: Enterprise-grade tool

7. **BiZZdesign**
   - **Type**: Commercial
   - **Use**: Enterprise architecture management
   - **Focus**: TOGAF, ArchiMate

## Cloud Architecture Tools

### Multi-Cloud Management

8. **Terraform by HashiCorp**
   - **Type**: Free (open-source) and paid tiers
   - **Use**: Infrastructure as Code, multi-cloud
   - **Link**: [terraform.io](https://www.terraform.io)
   - **Recommendation**: Essential for IaC

9. **Pulumi**
   - **Type**: Free (open-source) and paid tiers
   - **Use**: Infrastructure as Code, any language
   - **Link**: [pulumi.com](https://www.pulumi.com)
   - **Languages**: Python, TypeScript, Go, C#

10. **Crossplane**
    - **Type**: Free, open-source (CNCF)
    - **Use**: Kubernetes-native IaC
    - **Link**: [crossplane.io](https://www.crossplane.io)

### Cloud Provider Tools

#### AWS

11. **AWS Well-Architected Tool**
    - **Type**: Free (AWS Console)
    - **Use**: Architecture review and guidance
    - **Link**: [AWS Console](https://console.aws.amazon.com/wellarchitected/)

12. **AWS CloudFormation**
    - **Type**: Free (pay for resources)
    - **Use**: Infrastructure as Code for AWS

13. **AWS CDK (Cloud Development Kit)**
    - **Type**: Free, open-source
    - **Use**: Define infrastructure in code
    - **Languages**: TypeScript, Python, Java, C#

#### GCP

14. **GCP Architecture Center**
    - **Type**: Free (documentation)
    - **Use**: Reference architectures and best practices
    - **Link**: [cloud.google.com/architecture](https://cloud.google.com/architecture)

15. **GCP Deployment Manager**
    - **Type**: Free (pay for resources)
    - **Use**: Infrastructure as Code for GCP

#### Azure

16. **Azure Architecture Center**
    - **Type**: Free (documentation)
    - **Use**: Reference architectures
    - **Link**: [docs.microsoft.com/azure/architecture](https://docs.microsoft.com/en-us/azure/architecture/)

17. **Azure Resource Manager (ARM) Templates**
    - **Type**: Free
    - **Use**: Infrastructure as Code for Azure

## Kubernetes and Container Tools

18. **kubectl**
    - **Type**: Free, open-source
    - **Use**: Kubernetes CLI
    - **Recommendation**: Essential

19. **Helm**
    - **Type**: Free, open-source (CNCF)
    - **Use**: Kubernetes package manager
    - **Link**: [helm.sh](https://helm.sh)

20. **Kustomize**
    - **Type**: Free, open-source
    - **Use**: Kubernetes configuration management
    - **Link**: [kustomize.io](https://kustomize.io)

21. **K9s**
    - **Type**: Free, open-source
    - **Use**: Terminal UI for Kubernetes
    - **Link**: [k9scli.io](https://k9scli.io)
    - **Recommendation**: Better UX than kubectl

22. **Lens**
    - **Type**: Free and paid tiers
    - **Use**: Kubernetes IDE
    - **Link**: [k8slens.dev](https://k8slens.dev)

## Cost Management and FinOps

23. **CloudHealth by VMware**
    - **Type**: Commercial
    - **Use**: Multi-cloud cost management
    - **Features**: Cost allocation, optimization, governance

24. **CloudCheckr**
    - **Type**: Commercial
    - **Use**: Cloud cost and security management
    - **Features**: Cost optimization, compliance

25. **Kubecost**
    - **Type**: Free and paid tiers
    - **Use**: Kubernetes cost monitoring
    - **Link**: [kubecost.com](https://www.kubecost.com)
    - **Recommendation**: Essential for K8s cost visibility

26. **Infracost**
    - **Type**: Free, open-source
    - **Use**: Cost estimates for Terraform
    - **Link**: [infracost.io](https://www.infracost.io)

### Native Cloud Cost Tools

27. **AWS Cost Explorer**
    - **Type**: Free (included with AWS)
    - **Use**: AWS cost analysis and forecasting

28. **GCP Cost Management**
    - **Type**: Free (included with GCP)
    - **Use**: GCP cost analysis and recommendations

29. **Azure Cost Management**
    - **Type**: Free (included with Azure)
    - **Use**: Azure cost analysis and budgets

## Monitoring and Observability

30. **Prometheus**
    - **Type**: Free, open-source (CNCF)
    - **Use**: Metrics collection and alerting
    - **Link**: [prometheus.io](https://prometheus.io)
    - **Recommendation**: Industry standard

31. **Grafana**
    - **Type**: Free, open-source
    - **Use**: Metrics visualization and dashboards
    - **Link**: [grafana.com](https://grafana.com)
    - **Recommendation**: Pair with Prometheus

32. **DataDog**
    - **Type**: Commercial ($15-$23/host/month)
    - **Use**: Enterprise observability platform
    - **Link**: [datadoghq.com](https://www.datadoghq.com)
    - **Features**: APM, logs, metrics, traces

33. **New Relic**
    - **Type**: Commercial
    - **Use**: Full-stack observability
    - **Features**: APM, infrastructure, logs

34. **Dynatrace**
    - **Type**: Commercial
    - **Use**: AI-powered observability
    - **Features**: Auto-discovery, AI analytics

35. **Jaeger**
    - **Type**: Free, open-source (CNCF)
    - **Use**: Distributed tracing
    - **Link**: [jaegertracing.io](https://www.jaegertracing.io)

36. **Zipkin**
    - **Type**: Free, open-source
    - **Use**: Distributed tracing
    - **Link**: [zipkin.io](https://zipkin.io)

## MLOps and ML Infrastructure

37. **MLflow**
    - **Type**: Free, open-source
    - **Use**: ML lifecycle management
    - **Link**: [mlflow.org](https://mlflow.org)
    - **Recommendation**: Essential for MLOps

38. **Kubeflow**
    - **Type**: Free, open-source
    - **Use**: ML workflows on Kubernetes
    - **Link**: [kubeflow.org](https://www.kubeflow.org)

39. **Weights & Biases**
    - **Type**: Free and paid tiers
    - **Use**: Experiment tracking and collaboration
    - **Link**: [wandb.ai](https://wandb.ai)

40. **Neptune.ai**
    - **Type**: Free and paid tiers
    - **Use**: ML metadata store

41. **DVC (Data Version Control)**
    - **Type**: Free, open-source
    - **Use**: Data and model versioning
    - **Link**: [dvc.org](https://dvc.org)

42. **Feast**
    - **Type**: Free, open-source
    - **Use**: Feature store
    - **Link**: [feast.dev](https://feast.dev)

## Security and Compliance

43. **Open Policy Agent (OPA)**
    - **Type**: Free, open-source (CNCF)
    - **Use**: Policy as code
    - **Link**: [openpolicyagent.org](https://www.openpolicyagent.org)

44. **Falco**
    - **Type**: Free, open-source (CNCF)
    - **Use**: Runtime security for Kubernetes
    - **Link**: [falco.org](https://falco.org)

45. **Trivy**
    - **Type**: Free, open-source
    - **Use**: Container security scanning
    - **Link**: [github.com/aquasecurity/trivy](https://github.com/aquasecurity/trivy)

46. **Snyk**
    - **Type**: Free and paid tiers
    - **Use**: Security scanning for code and containers
    - **Link**: [snyk.io](https://snyk.io)

47. **HashiCorp Vault**
    - **Type**: Free (open-source) and paid tiers
    - **Use**: Secrets management
    - **Link**: [vaultproject.io](https://www.vaultproject.io)

### Cloud Security Posture Management

48. **Prisma Cloud (Palo Alto)**
    - **Type**: Commercial
    - **Use**: Cloud security posture management

49. **Wiz**
    - **Type**: Commercial
    - **Use**: Cloud security platform

## Data and Streaming

50. **Apache Kafka**
    - **Type**: Free, open-source
    - **Use**: Event streaming platform
    - **Link**: [kafka.apache.org](https://kafka.apache.org)

51. **Apache Spark**
    - **Type**: Free, open-source
    - **Use**: Distributed data processing
    - **Link**: [spark.apache.org](https://spark.apache.org)

52. **Apache Airflow**
    - **Type**: Free, open-source
    - **Use**: Workflow orchestration
    - **Link**: [airflow.apache.org](https://airflow.apache.org)

53. **Delta Lake**
    - **Type**: Free, open-source
    - **Use**: Data lakehouse storage layer
    - **Link**: [delta.io](https://delta.io)

54. **Apache Iceberg**
    - **Type**: Free, open-source
    - **Use**: Table format for data lakes

## LLM and Vector Databases

55. **Pinecone**
    - **Type**: Commercial (managed service)
    - **Use**: Vector database for RAG
    - **Link**: [pinecone.io](https://www.pinecone.io)

56. **Weaviate**
    - **Type**: Free (open-source) and paid tiers
    - **Use**: Vector database
    - **Link**: [weaviate.io](https://weaviate.io)

57. **Milvus**
    - **Type**: Free, open-source
    - **Use**: Vector database
    - **Link**: [milvus.io](https://milvus.io)

58. **Chroma**
    - **Type**: Free, open-source
    - **Use**: Vector database
    - **Link**: [trychroma.com](https://www.trychroma.com)

59. **vLLM**
    - **Type**: Free, open-source
    - **Use**: LLM inference engine
    - **Link**: [github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)

60. **Text Generation Inference (TGI)**
    - **Type**: Free, open-source (Hugging Face)
    - **Use**: LLM serving
    - **Link**: [github.com/huggingface/text-generation-inference](https://github.com/huggingface/text-generation-inference)

## CI/CD and GitOps

61. **GitHub Actions**
    - **Type**: Free for public repos, paid for private
    - **Use**: CI/CD automation
    - **Link**: [github.com/features/actions](https://github.com/features/actions)

62. **GitLab CI**
    - **Type**: Free and paid tiers
    - **Use**: CI/CD automation

63. **Jenkins**
    - **Type**: Free, open-source
    - **Use**: CI/CD automation
    - **Link**: [jenkins.io](https://www.jenkins.io)

64. **ArgoCD**
    - **Type**: Free, open-source (CNCF)
    - **Use**: GitOps for Kubernetes
    - **Link**: [argoproj.github.io/cd](https://argoproj.github.io/cd/)

65. **Flux**
    - **Type**: Free, open-source (CNCF)
    - **Use**: GitOps for Kubernetes
    - **Link**: [fluxcd.io](https://fluxcd.io)

## Documentation and Knowledge Management

66. **Confluence**
    - **Type**: Commercial (Atlassian)
    - **Use**: Team documentation and collaboration

67. **Notion**
    - **Type**: Free and paid tiers
    - **Use**: Knowledge management and documentation

68. **MkDocs**
    - **Type**: Free, open-source
    - **Use**: Documentation from Markdown
    - **Link**: [mkdocs.org](https://www.mkdocs.org)

69. **Docusaurus**
    - **Type**: Free, open-source (Meta)
    - **Use**: Documentation websites
    - **Link**: [docusaurus.io](https://docusaurus.io)

## Performance and Load Testing

70. **Locust**
    - **Type**: Free, open-source
    - **Use**: Load testing
    - **Link**: [locust.io](https://locust.io)

71. **k6**
    - **Type**: Free (open-source) and paid tiers
    - **Use**: Load testing as code
    - **Link**: [k6.io](https://k6.io)

72. **Apache JMeter**
    - **Type**: Free, open-source
    - **Use**: Performance testing

## Collaboration and Communication

73. **Slack**
    - **Type**: Free and paid tiers
    - **Use**: Team communication

74. **Microsoft Teams**
    - **Type**: Part of Microsoft 365
    - **Use**: Team collaboration

75. **Miro**
    - **Type**: Free and paid tiers
    - **Use**: Online whiteboarding and workshops

## Recommended Toolset by Phase

### Design Phase
- Draw.io or Lucidchart for diagrams
- Confluence or Notion for documentation
- Miro for workshops and brainstorming

### Implementation Phase
- Terraform or Pulumi for IaC
- GitHub/GitLab for version control
- Kubernetes + Helm for orchestration
- MLflow for ML lifecycle

### Operations Phase
- Prometheus + Grafana for monitoring
- DataDog or New Relic for enterprise observability
- Kubecost for cost monitoring
- ArgoCD for GitOps

### Security Phase
- OPA for policy enforcement
- Vault for secrets management
- Trivy or Snyk for security scanning
- Cloud provider security tools

## Tool Selection Criteria

When selecting tools, consider:

1. **Functionality**: Does it meet requirements?
2. **Scalability**: Can it handle growth?
3. **Integration**: Does it integrate with existing tools?
4. **Cost**: What's the TCO (licensing, training, maintenance)?
5. **Support**: What support is available?
6. **Community**: Is there an active community?
7. **Vendor Lock-in**: Can you migrate away if needed?
8. **Learning Curve**: How long to become productive?

## Free vs Paid Considerations

### When Free/Open-Source is Sufficient
- Small to medium organizations
- Limited budget
- Strong in-house expertise
- Control and customization important

### When Paid Tools Make Sense
- Enterprise requirements
- Need for vendor support
- Compliance and audit requirements
- Time-to-value critical
- Limited in-house expertise

---

**Tool Updates**: This list is maintained regularly as tools evolve.

**Suggestions**: Missing a tool? Submit a pull request!
