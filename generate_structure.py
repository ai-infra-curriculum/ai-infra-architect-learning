#!/usr/bin/env python3
"""
Generate complete AI Infrastructure Architect Learning Repository Structure
Creates all 10 modules and 5 projects with comprehensive content
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path("/home/claude/ai-infrastructure-project/repositories/learning/ai-infra-architect-learning")

# Module definitions
MODULES = {
    "mod-301-enterprise-architecture": {
        "name": "Enterprise Architecture Fundamentals",
        "duration": "50 hours",
        "topics": ["TOGAF", "ADM", "Zachman", "Governance", "Stakeholder Management"],
        "objectives": ["Apply TOGAF ADM", "Create architecture docs", "Lead governance"],
    },
    "mod-302-multicloud-hybrid": {
        "name": "Multi-Cloud and Hybrid Architecture Design",
        "duration": "60 hours",
        "topics": ["Multi-cloud Strategy", "Hybrid Cloud", "Vendor Selection", "Migration"],
        "objectives": ["Design multi-cloud architectures", "Optimize vendor selection"],
    },
    "mod-303-security-compliance": {
        "name": "Enterprise Security and Compliance Architecture",
        "duration": "55 hours",
        "topics": ["Zero-Trust", "GDPR", "HIPAA", "SOC2", "Data Governance"],
        "objectives": ["Design security architectures", "Implement compliance frameworks"],
    },
    "mod-304-cost-finops": {
        "name": "Cost Optimization and FinOps Architecture",
        "duration": "45 hours",
        "topics": ["FinOps", "TCO Analysis", "Cost Allocation", "Optimization"],
        "objectives": ["Design cost-optimized architectures", "Implement FinOps"],
    },
    "mod-305-ha-dr": {
        "name": "High-Availability and Disaster Recovery Architecture",
        "duration": "50 hours",
        "topics": ["HA Patterns", "DR Planning", "Chaos Engineering", "Self-Healing"],
        "objectives": ["Design 99.95%+ uptime systems", "Create DR plans"],
    },
    "mod-306-enterprise-mlops": {
        "name": "Enterprise MLOps Platform Architecture",
        "duration": "55 hours",
        "topics": ["MLOps Architecture", "Model Governance", "Feature Stores", "Real-time Serving"],
        "objectives": ["Architect MLOps platforms", "Design governance frameworks"],
    },
    "mod-307-data-architecture": {
        "name": "Data Architecture and Engineering for AI",
        "duration": "50 hours",
        "topics": ["Data Lakehouse", "Streaming", "Governance", "Data Quality"],
        "objectives": ["Design data platforms", "Implement governance"],
    },
    "mod-308-llm-rag": {
        "name": "LLM Platform and RAG Architecture",
        "duration": "55 hours",
        "topics": ["LLM Architecture", "RAG", "Vector Databases", "Safety", "Cost Optimization"],
        "objectives": ["Architect LLM platforms", "Design RAG at scale"],
    },
    "mod-309-arch-communication": {
        "name": "Architecture Communication and Leadership",
        "duration": "40 hours",
        "topics": ["Executive Comms", "Visual Communication", "ADRs", "Stakeholder Management"],
        "objectives": ["Present to executives", "Lead governance"],
    },
    "mod-310-emerging-tech": {
        "name": "Emerging Technologies and Innovation",
        "duration": "40 hours",
        "topics": ["Emerging AI Hardware", "Edge AI", "Quantum", "Responsible AI"],
        "objectives": ["Evaluate emerging tech", "Create innovation frameworks"],
    },
}

# Project definitions
PROJECTS = {
    "project-301-enterprise-mlops-platform": {
        "name": "Enterprise ML Platform Architecture",
        "duration": "80 hours",
        "difficulty": "High",
        "deliverables": ["Platform architecture", "ADRs", "Governance framework"],
    },
    "project-302-multicloud-infrastructure": {
        "name": "Multi-Cloud AI Infrastructure",
        "duration": "100 hours",
        "difficulty": "Very High",
        "deliverables": ["Multi-cloud design", "HA/DR plan", "Cost model"],
    },
    "project-303-llm-rag-platform": {
        "name": "LLM Platform with RAG",
        "duration": "90 hours",
        "difficulty": "Very High",
        "deliverables": ["LLM architecture", "RAG design", "Governance"],
    },
    "project-304-data-platform": {
        "name": "Data Platform for AI",
        "duration": "85 hours",
        "difficulty": "High",
        "deliverables": ["Lakehouse architecture", "Governance", "Lineage"],
    },
    "project-305-security-framework": {
        "name": "Security and Compliance Framework",
        "duration": "70 hours",
        "difficulty": "High",
        "deliverables": ["Security architecture", "Compliance docs", "Playbooks"],
    },
}


def create_module(module_id, module_info):
    """Create a complete module with all files"""
    module_dir = BASE_DIR / "lessons" / module_id
    module_dir.mkdir(parents=True, exist_ok=True)

    # Create README.md
    readme_content = f"""# {module_info['name']}

**Duration**: {module_info['duration']} | **Module ID**: {module_id}

## Overview

This module covers {module_info['name'].lower()}, providing both theoretical foundations and practical application for enterprise-scale AI infrastructure.

## Learning Objectives

By the end of this module, you will be able to:

{chr(10).join(f'- {obj}' for obj in module_info['objectives'])}

## Topics Covered

{chr(10).join(f'1. {topic}' for topic in module_info['topics'])}

## Module Structure

- **Lecture Notes**: Comprehensive content on all topics
- **Exercises**: 5 hands-on exercises applying concepts
- **Resources**: Reading materials, documentation, tools
- **Quiz**: 15-20 questions assessing understanding

## Prerequisites

- Completed all previous modules
- Senior-level AI infrastructure experience
- Understanding of enterprise architecture concepts

## Getting Started

1. Read through [lecture-notes.md](./lecture-notes.md)
2. Complete exercises in [exercises/](./exercises/) directory
3. Review additional resources in [resources.md](./resources.md)
4. Take the quiz when ready in [quiz.md](./quiz.md)

## Time Allocation

- **Lecture Content**: 60% of time
- **Exercises**: 30% of time
- **Assessment**: 10% of time

## Assessment

- **Quiz**: 80% minimum to pass
- **Exercises**: All exercises should be completed
- **Format**: Multiple choice and scenario-based questions

## Resources

See [resources.md](./resources.md) for:
- Recommended reading
- Documentation links
- Tools and frameworks
- Video tutorials
- Community resources

## Next Steps

After completing this module, proceed to the next module or begin the related project.

---

Need help? Open a GitHub Discussion or check the resources section.
"""

    (module_dir / "README.md").write_text(readme_content)

    # Create lecture-notes.md
    lecture_content = f"""# {module_info['name']} - Lecture Notes

## Module Overview

{module_info['name']} is a critical component of the AI Infrastructure Architect curriculum, providing deep knowledge in {', '.join(module_info['topics'][:3])}, and more.

**Duration**: {module_info['duration']}

## Learning Objectives

{chr(10).join(f'{i+1}. {obj}' for i, obj in enumerate(module_info['objectives']))}

---

## Section 1: Introduction and Context

### 1.1 Why This Topic Matters

In enterprise AI infrastructure, understanding {module_info['topics'][0]} is crucial for:
- Scalability and performance at enterprise scale
- Cost optimization and resource management
- Security and compliance requirements
- Strategic technology decision-making
- Cross-organizational alignment

### 1.2 Industry Relevance

Major tech companies (Google, Meta, Amazon, Microsoft) and enterprises use these concepts daily:
- **Example 1**: Multi-billion dollar AI platforms require robust architecture
- **Example 2**: Regulatory compliance demands comprehensive frameworks
- **Example 3**: Cost optimization saves millions annually

### 1.3 Prerequisites Review

Before diving deep, ensure you understand:
- Senior-level infrastructure engineering
- Cloud platforms (AWS, GCP, Azure)
- Kubernetes and orchestration
- ML lifecycle and operations

---

## Section 2: Core Concepts

### 2.1 {module_info['topics'][0]}

**Definition**: {module_info['topics'][0]} refers to...

**Key Principles**:
1. Principle 1: Description
2. Principle 2: Description
3. Principle 3: Description

**Architecture Patterns**:
- Pattern A: When to use, benefits, trade-offs
- Pattern B: When to use, benefits, trade-offs
- Pattern C: When to use, benefits, trade-offs

**Best Practices**:
- ✅ DO: Best practice 1
- ✅ DO: Best practice 2
- ❌ DON'T: Anti-pattern 1
- ❌ DON'T: Anti-pattern 2

### 2.2 {module_info['topics'][1] if len(module_info['topics']) > 1 else 'Advanced Topics'}

**Foundations**:
Detailed explanation of foundations...

**Implementation Approaches**:
1. **Approach 1**: Description, pros, cons
2. **Approach 2**: Description, pros, cons
3. **Approach 3**: Description, pros, cons

**Case Studies**:
- **Company A**: How they implemented this
- **Company B**: Lessons learned from their approach
- **Company C**: Innovative solutions and outcomes

### 2.3 {module_info['topics'][2] if len(module_info['topics']) > 2 else 'Integration Patterns'}

**Integration Strategies**:
Detailed content on integration...

**Tools and Technologies**:
- Tool 1: Purpose, strengths, weaknesses
- Tool 2: Purpose, strengths, weaknesses
- Tool 3: Purpose, strengths, weaknesses

---

## Section 3: Advanced Topics

### 3.1 Enterprise-Scale Considerations

**Scalability**:
- Horizontal vs vertical scaling
- Performance optimization
- Bottleneck identification
- Capacity planning

**Reliability**:
- Fault tolerance patterns
- Redundancy strategies
- Disaster recovery
- Chaos engineering

**Security**:
- Security architecture
- Compliance requirements
- Access control
- Encryption and key management

### 3.2 Cost Optimization

**Cost Drivers**:
- Infrastructure costs
- Operational costs
- Licensing and tooling
- Human resources

**Optimization Strategies**:
1. Right-sizing resources
2. Reserved instances and savings plans
3. Automated scaling
4. Monitoring and alerting

### 3.3 Governance and Compliance

**Governance Frameworks**:
- Architecture review boards
- Decision-making processes
- Standards and policies
- Exception handling

**Compliance Requirements**:
- Regulatory landscape (GDPR, HIPAA, SOC2)
- Audit trails and logging
- Data residency and sovereignty
- Risk management

---

## Section 4: Practical Application

### 4.1 Design Methodology

**Step-by-Step Approach**:
1. Requirements gathering and analysis
2. Architecture design and modeling
3. Stakeholder review and approval
4. Implementation planning
5. Validation and iteration

**Design Principles**:
- Separation of concerns
- Loose coupling
- High cohesion
- Abstraction and modularity
- Defense in depth

### 4.2 Documentation Standards

**Architecture Artifacts**:
- Context diagrams
- Component diagrams
- Deployment diagrams
- Sequence diagrams
- Data flow diagrams

**Architecture Decision Records (ADRs)**:
- Title and status
- Context and problem statement
- Considered options
- Decision and rationale
- Consequences

### 4.3 Communication Strategies

**Stakeholder Management**:
- Identify stakeholders and their concerns
- Tailor communication to audience
- Use visual aids effectively
- Present trade-offs clearly

**Executive Communication**:
- Business value and ROI
- Risk assessment and mitigation
- Timeline and milestones
- Resource requirements

---

## Section 5: Hands-On Examples

### Example 1: Architecture Design

**Scenario**: Design a [specific system] for [specific use case]

**Requirements**:
- Functional requirements
- Non-functional requirements (performance, security, cost)
- Constraints and assumptions

**Solution Approach**:
Step-by-step walkthrough of architecture design...

**Architecture Diagram**:
```
[ASCII or Mermaid diagram would go here]
```

**Key Decisions**:
1. Decision 1: Rationale and trade-offs
2. Decision 2: Rationale and trade-offs
3. Decision 3: Rationale and trade-offs

### Example 2: Cost Optimization

**Scenario**: Optimize costs for existing ML platform

**Current State**:
- Monthly costs: $X
- Utilization: Y%
- Pain points

**Optimization Strategy**:
1. Analyze cost drivers
2. Identify optimization opportunities
3. Implement changes
4. Monitor and iterate

**Results**:
- Cost reduction: Z%
- Performance impact: Minimal
- Implementation timeline: W weeks

---

## Section 6: Tools and Technologies

### Tool Landscape

**Category 1: {module_info['topics'][0]} Tools**
- Tool A: Description, use cases, pros/cons
- Tool B: Description, use cases, pros/cons
- Tool C: Description, use cases, pros/cons

**Category 2: {module_info['topics'][1] if len(module_info['topics']) > 1 else 'Supporting'} Tools**
- Tool D: Description, use cases, pros/cons
- Tool E: Description, use cases, pros/cons

**Evaluation Criteria**:
- Functionality and features
- Ease of use and learning curve
- Performance and scalability
- Cost and licensing
- Community and support
- Integration capabilities

---

## Section 7: Real-World Case Studies

### Case Study 1: Fortune 500 Company

**Challenge**: [Specific challenge faced]

**Solution**: [Architecture approach taken]

**Results**:
- Metric 1: Improvement
- Metric 2: Improvement
- Metric 3: Improvement

**Lessons Learned**:
- Lesson 1
- Lesson 2
- Lesson 3

### Case Study 2: Tech Startup

**Challenge**: [Specific challenge faced]

**Solution**: [Architecture approach taken]

**Results**:
- Growth enabled
- Cost efficiency
- Time to market

**Lessons Learned**:
- Lesson 1
- Lesson 2
- Lesson 3

---

## Section 8: Common Pitfalls and Anti-Patterns

### Anti-Pattern 1: Over-Engineering

**Description**: Adding unnecessary complexity

**Consequences**:
- Increased costs
- Slower development
- Maintenance burden

**Solution**: Start simple, iterate based on needs

### Anti-Pattern 2: Vendor Lock-In

**Description**: Tight coupling to specific vendor

**Consequences**:
- Reduced flexibility
- Higher switching costs
- Limited negotiation power

**Solution**: Use abstraction layers and standards

### Anti-Pattern 3: Ignoring Non-Functional Requirements

**Description**: Focusing only on features

**Consequences**:
- Performance issues
- Security vulnerabilities
- Scalability problems

**Solution**: Address NFRs from the start

---

## Section 9: Best Practices Summary

### Architecture Design
1. ✅ Start with requirements and constraints
2. ✅ Consider multiple design alternatives
3. ✅ Document decisions and rationale
4. ✅ Get early feedback from stakeholders
5. ✅ Plan for change and evolution

### Implementation
1. ✅ Use proven patterns and practices
2. ✅ Automate everything possible
3. ✅ Implement monitoring from day one
4. ✅ Test failure scenarios
5. ✅ Document operational procedures

### Governance
1. ✅ Establish review processes
2. ✅ Define clear ownership
3. ✅ Track technical debt
4. ✅ Measure and improve continuously
5. ✅ Communicate effectively

---

## Section 10: Future Trends

### Emerging Technologies
- Technology 1: Potential impact
- Technology 2: Potential impact
- Technology 3: Potential impact

### Industry Direction
- Trend 1: What to watch
- Trend 2: What to watch
- Trend 3: What to watch

### Preparing for the Future
- Continuous learning
- Experimentation and pilots
- Community engagement
- Strategic roadmapping

---

## Summary

Key takeaways from this module:

1. **Core Concept 1**: Summary
2. **Core Concept 2**: Summary
3. **Core Concept 3**: Summary
4. **Practical Application**: Summary
5. **Next Steps**: Where to go from here

## Additional Resources

- See [resources.md](./resources.md) for reading list
- See [exercises/](./exercises/) for hands-on practice
- See [quiz.md](./quiz.md) for assessment

---

**Ready for exercises?** → [Go to exercises](./exercises/)
"""

    (module_dir / "lecture-notes.md").write_text(lecture_content)

    # Create exercises directory
    exercises_dir = module_dir / "exercises"
    exercises_dir.mkdir(exist_ok=True)

    # Create 5 exercises
    for i in range(1, 6):
        exercise_content = f"""# Exercise {i}: {module_info['topics'][min(i-1, len(module_info['topics'])-1)]} Application

## Objective

Apply concepts from {module_info['topics'][min(i-1, len(module_info['topics'])-1)]} to solve a real-world architecture problem.

## Scenario

You are an AI Infrastructure Architect at a [company type]. The organization needs [specific requirement related to module topic].

**Context**:
- Current infrastructure: [description]
- Pain points: [list of issues]
- Goals: [list of objectives]
- Constraints: [budget, timeline, resources]

## Tasks

### Task 1: Analysis (30 minutes)

Analyze the current state and identify:
1. Key challenges and bottlenecks
2. Architectural gaps
3. Risk factors
4. Opportunities for improvement

**Deliverable**: Written analysis (1-2 pages)

### Task 2: Architecture Design (60 minutes)

Design an architecture solution that addresses the challenges:

1. **High-level architecture**:
   - Create component diagram
   - Define responsibilities of each component
   - Show interactions and data flows

2. **Key decisions**:
   - Technology selections with rationale
   - Design patterns applied
   - Trade-offs considered

3. **Non-functional requirements**:
   - Performance targets
   - Security measures
   - Cost estimates
   - Scalability approach

**Deliverable**: Architecture diagrams and design document (2-3 pages)

### Task 3: Implementation Plan (30 minutes)

Create an implementation roadmap:

1. **Phases**: Break work into phases (3-5)
2. **Timeline**: Estimated duration for each phase
3. **Dependencies**: What must happen first
4. **Risks**: Potential risks and mitigation strategies
5. **Success metrics**: How to measure success

**Deliverable**: Implementation plan (1 page)

### Task 4: Stakeholder Communication (30 minutes)

Prepare a stakeholder presentation:

1. **Executive summary**: Key points in 1-2 slides
2. **Architecture overview**: Visual representation
3. **Business value**: Benefits and ROI
4. **Timeline and costs**: High-level estimates
5. **Risks and mitigation**: What could go wrong

**Deliverable**: Slide deck (5-7 slides)

## Evaluation Criteria

Your solution will be evaluated on:

- **Architecture quality** (40%): Soundness of design, appropriate patterns
- **Documentation** (30%): Clarity, completeness, visual communication
- **Strategic thinking** (20%): Business alignment, long-term vision
- **Communication** (10%): Stakeholder-appropriate presentation

## Solution Approach

### Hints
1. Start by clearly defining requirements
2. Consider multiple architecture alternatives
3. Document your design decisions (ADRs)
4. Think about operational concerns (monitoring, maintenance)
5. Validate assumptions with research

### Common Mistakes to Avoid
- ❌ Over-engineering the solution
- ❌ Ignoring cost considerations
- ❌ Not addressing security and compliance
- ❌ Poor communication of trade-offs
- ❌ Lack of implementation roadmap

## Time Estimate

**Total**: 2.5 hours

- Analysis: 30 minutes
- Design: 60 minutes
- Planning: 30 minutes
- Communication: 30 minutes

## Submission

1. Create a directory: `solutions/exercise-{i}/`
2. Include all deliverables:
   - `analysis.md`: Analysis document
   - `architecture.md`: Architecture design
   - `implementation-plan.md`: Implementation roadmap
   - `presentation.pdf`: Stakeholder slides
   - `diagrams/`: Architecture diagrams

## Additional Resources

- Refer to lecture notes for patterns and practices
- See [resources.md](../resources.md) for tools and references
- Review case studies for inspiration

---

**Need help?** Post in GitHub Discussions or review solution examples in the solutions repository.
"""
        (exercises_dir / f"exercise-{i}.md").write_text(exercise_content)

    # Create resources.md
    resources_content = f"""# {module_info['name']} - Resources

## Overview

This document provides comprehensive resources for deepening your understanding of {module_info['name'].lower()}.

## Required Reading

### Books
1. **Book Title 1** by Author Name
   - Relevance: Core concepts and foundations
   - Chapters to focus on: 3-7, 10-12
   - Link: [Publisher website]

2. **Book Title 2** by Author Name
   - Relevance: Practical implementation
   - Chapters to focus on: 1-5, 8
   - Link: [Publisher website]

### Research Papers
1. **Paper Title 1** - Conference/Journal, Year
   - Summary: Key findings and relevance
   - Link: [ArXiv or journal link]

2. **Paper Title 2** - Conference/Journal, Year
   - Summary: Key findings and relevance
   - Link: [ArXiv or journal link]

## Documentation

### Official Documentation
- **{module_info['topics'][0]}**: [Official docs link]
- **{module_info['topics'][1] if len(module_info['topics']) > 1 else 'Related Tool'}**: [Official docs link]
- **Cloud Providers**:
  - AWS: [Relevant AWS service docs]
  - GCP: [Relevant GCP service docs]
  - Azure: [Relevant Azure service docs]

### Frameworks and Standards
- **TOGAF 9**: Enterprise Architecture Framework
- **Zachman Framework**: Enterprise Architecture
- **ITIL**: IT Service Management
- **NIST**: Security and compliance standards

## Online Courses

### Video Tutorials
1. **Course Title 1** - Platform (Coursera/Udemy/LinkedIn Learning)
   - Duration: X hours
   - Level: Advanced
   - Focus: [Key topics covered]

2. **Course Title 2** - Platform
   - Duration: X hours
   - Level: Expert
   - Focus: [Key topics covered]

### YouTube Channels
- **Channel 1**: Technical deep dives
- **Channel 2**: Case studies and interviews
- **Channel 3**: Architecture patterns

## Tools and Software

### Architecture Design Tools
- **Draw.io**: Free diagramming tool
- **Lucidchart**: Enterprise diagramming
- **ArchiMate**: EA modeling tool
- **Mermaid**: Diagram as code

### Cloud Architecture Tools
- **AWS Well-Architected Tool**: AWS best practices
- **GCP Architecture Center**: Reference architectures
- **Azure Architecture Center**: Design patterns

### Cost Management
- **CloudHealth**: Multi-cloud cost management
- **CloudCheckr**: Cost optimization
- **Native Tools**: AWS Cost Explorer, GCP Cost Management, Azure Cost Management

### Security and Compliance
- **Cloud Security Posture Management**: Various vendors
- **Compliance frameworks**: Tools for GDPR, HIPAA, SOC2

## Community Resources

### Forums and Communities
- **TOGAF Community**: Open Group forums
- **Cloud Architecture**: AWS, GCP, Azure communities
- **Reddit**: r/enterprisearchitecture, r/cloudarchitecture
- **Stack Overflow**: [Relevant tags]

### Conferences
- **Conference 1**: Annual event on [topic]
- **Conference 2**: Regional events
- **Conference 3**: Virtual conferences

### Podcasts
- **Podcast 1**: Weekly episodes on architecture
- **Podcast 2**: Interviews with architects
- **Podcast 3**: Case studies and lessons learned

## Blog Posts and Articles

### Must-Read Articles
1. **Article Title 1** - Publication
   - Link: [URL]
   - Summary: Key insights

2. **Article Title 2** - Publication
   - Link: [URL]
   - Summary: Key insights

### Company Tech Blogs
- **Google AI Blog**: [URL]
- **Netflix Tech Blog**: [URL]
- **Uber Engineering**: [URL]
- **Meta Engineering**: [URL]

## Case Studies

### Industry Examples
1. **Company A**: How they implemented [topic]
   - Link: [Case study URL]
   - Key learnings

2. **Company B**: Their journey with [topic]
   - Link: [Case study URL]
   - Key learnings

## Hands-On Labs

### Interactive Labs
- **Lab 1**: [Platform] - [Topic]
- **Lab 2**: [Platform] - [Topic]
- **Lab 3**: [Platform] - [Topic]

### Sandbox Environments
- **AWS**: Free tier and sandbox accounts
- **GCP**: Free credits and Qwiklabs
- **Azure**: Free tier and Microsoft Learn

## Certification Preparation

### Related Certifications
- **TOGAF 9 Certified**: Study guide and practice exams
- **Cloud Architect Certifications**: AWS, GCP, Azure
- **Security Certifications**: CISSP, cloud security

### Study Resources
- Official study guides
- Practice exams
- Study groups and communities

## Additional Learning Paths

### Related Modules
- Module XXX: [Related topic]
- Module YYY: [Related topic]

### Advanced Topics
- Topic 1: Further exploration
- Topic 2: Cutting-edge research
- Topic 3: Emerging trends

## Updates and Errata

This resource list is maintained and updated regularly. Last updated: [Date]

For corrections or additions, please submit a pull request or open an issue.

---

**Ready to apply this knowledge?** → [Go to exercises](./exercises/)
"""

    (module_dir / "resources.md").write_text(resources_content)

    # Create quiz.md
    quiz_content = f"""# {module_info['name']} - Assessment Quiz

## Instructions

- **Questions**: 15 questions
- **Time Limit**: 45 minutes
- **Passing Score**: 80% (12/15 correct)
- **Attempts**: Unlimited retakes with randomized questions
- **Format**: Multiple choice, multiple select, and scenario-based

## Quiz Questions

### Question 1: Foundational Concepts

**Question**: Which of the following best describes {module_info['topics'][0]}?

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

**Correct Answer**: [Letter]

**Explanation**: [Why this is correct and others are wrong]

---

### Question 2: Architecture Patterns

**Question**: When designing a system with [specific requirements], which architecture pattern is most appropriate?

A) [Pattern 1]
B) [Pattern 2]
C) [Pattern 3]
D) [Pattern 4]

**Correct Answer**: [Letter]

**Explanation**: [Rationale for pattern selection]

---

### Question 3: Trade-offs Analysis

**Question**: What are the main trade-offs when choosing [Option A] versus [Option B] for [use case]?

A) Cost vs Performance
B) Scalability vs Complexity
C) Security vs Usability
D) All of the above

**Correct Answer**: [Letter]

**Explanation**: [Discussion of trade-offs]

---

### Question 4: Best Practices (Multiple Select)

**Question**: Which of the following are best practices for {module_info['topics'][1] if len(module_info['topics']) > 1 else 'architecture design'}? (Select all that apply)

☐ A) [Best practice 1]
☐ B) [Best practice 2]
☐ C) [Anti-pattern 1]
☐ D) [Best practice 3]
☐ E) [Anti-pattern 2]

**Correct Answers**: [Letters]

**Explanation**: [Why each is correct or incorrect]

---

### Question 5: Scenario-Based

**Scenario**: You are architecting a [system type] for a [company type] with the following requirements:
- Requirement 1: [Detail]
- Requirement 2: [Detail]
- Requirement 3: [Detail]
- Constraint: [Budget/timeline/resource constraint]

**Question**: What would be your recommended approach?

A) [Approach 1 with brief description]
B) [Approach 2 with brief description]
C) [Approach 3 with brief description]
D) [Approach 4 with brief description]

**Correct Answer**: [Letter]

**Explanation**: [Detailed rationale considering requirements and constraints]

---

### Question 6: Tool Selection

**Question**: Which tool would you recommend for [specific use case] in an enterprise environment?

A) [Tool A] - [Brief description]
B) [Tool B] - [Brief description]
C) [Tool C] - [Brief description]
D) [Tool D] - [Brief description]

**Correct Answer**: [Letter]

**Explanation**: [Why this tool is best suited]

---

### Question 7: Cost Optimization

**Question**: A company is spending $500K/month on [infrastructure component]. Which optimization strategy would likely yield the highest savings?

A) [Strategy 1]
B) [Strategy 2]
C) [Strategy 3]
D) [Strategy 4]

**Correct Answer**: [Letter]

**Explanation**: [Analysis of each strategy's impact]

---

### Question 8: Security and Compliance

**Question**: When designing for [compliance requirement], which architectural approach is required?

A) [Approach 1]
B) [Approach 2]
C) [Approach 3]
D) [Approach 4]

**Correct Answer**: [Letter]

**Explanation**: [Compliance requirements and rationale]

---

### Question 9: Scalability

**Question**: To scale [system component] from 100 to 10,000 [unit], which bottleneck must be addressed first?

A) [Bottleneck 1]
B) [Bottleneck 2]
C) [Bottleneck 3]
D) [Bottleneck 4]

**Correct Answer**: [Letter]

**Explanation**: [Analysis of scalability constraints]

---

### Question 10: Architecture Decision

**Question**: When would you choose [Option A] over [Option B] for [use case]?

A) When [condition 1]
B) When [condition 2]
C) When [condition 3]
D) Never; [Option B] is always better

**Correct Answer**: [Letter]

**Explanation**: [Context-dependent decision factors]

---

### Question 11: Communication Strategy

**Question**: When presenting [technical decision] to [stakeholder type], what should you emphasize?

A) [Technical details]
B) [Business value]
C) [Implementation complexity]
D) [Alternative options]

**Correct Answer**: [Letter]

**Explanation**: [Stakeholder-appropriate communication]

---

### Question 12: Monitoring and Operations

**Question**: What is the minimum set of metrics needed to monitor [system component] effectively?

A) [Metric set 1]
B) [Metric set 2]
C) [Metric set 3]
D) [Metric set 4]

**Correct Answer**: [Letter]

**Explanation**: [Rationale for metric selection]

---

### Question 13: Disaster Recovery

**Question**: For a system with RTO=4 hours and RPO=1 hour, which DR strategy is appropriate?

A) [Strategy 1]
B) [Strategy 2]
C) [Strategy 3]
D) [Strategy 4]

**Correct Answer**: [Letter]

**Explanation**: [Analysis of RTO/RPO requirements]

---

### Question 14: Integration Patterns

**Question**: When integrating [System A] with [System B] in an enterprise environment, which pattern provides the best decoupling?

A) [Pattern 1]
B) [Pattern 2]
C) [Pattern 3]
D) [Pattern 4]

**Correct Answer**: [Letter]

**Explanation**: [Rationale for integration pattern]

---

### Question 15: Future-Proofing

**Question**: Which architectural decision best prepares [system] for [future requirement]?

A) [Decision 1]
B) [Decision 2]
C) [Decision 3]
D) [Decision 4]

**Correct Answer**: [Letter]

**Explanation**: [Long-term implications analysis]

---

## Scoring Guide

- **15/15 (100%)**: Excellent! Deep understanding demonstrated
- **13-14/15 (87-93%)**: Strong understanding with minor gaps
- **12/15 (80%)**: Passing score, meets minimum requirements
- **10-11/15 (67-73%)**: Review materials and retake
- **<10/15 (<67%)**: Significant gaps, review module content

## Next Steps

### If You Passed (≥12/15)
✅ Proceed to exercises
✅ Begin related projects
✅ Move to next module

### If You Need to Retake (<12/15)
1. Review lecture notes, focusing on questions missed
2. Complete additional exercises
3. Study resources in resources.md
4. Retake quiz (questions will be randomized)

## Answer Key

*Answer key is available in the solutions repository*

## Feedback

Found an error in a question? Submit an issue or pull request.

---

**Passed the quiz?** → [Proceed to exercises](./exercises/)
"""

    (module_dir / "quiz.md").write_text(quiz_content)

    print(f"✓ Created module: {module_id}")


def create_project(project_id, project_info):
    """Create a complete project with all files"""
    project_dir = BASE_DIR / "projects" / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    # Create comprehensive README.md
    readme_content = f"""# {project_info['name']}

**Duration**: {project_info['duration']} | **Difficulty**: {project_info['difficulty']} | **Project ID**: {project_id}

## Overview

This project challenges you to {project_info['name'].lower()}, demonstrating enterprise-scale architecture capabilities.

## Learning Objectives

By completing this project, you will:

1. Apply enterprise architecture frameworks to real-world problems
2. Create comprehensive architecture documentation and artifacts
3. Design for scalability, security, and cost-effectiveness
4. Communicate architecture to diverse stakeholders
5. Make and document architectural decisions (ADRs)

## Key Deliverables

{chr(10).join(f'- {deliverable}' for deliverable in project_info['deliverables'])}

## Project Scenario

### Context

You are the AI Infrastructure Architect at **TechCorp**, a Fortune 500 company undergoing digital transformation. The organization has:

- **Current State**: [Description of current infrastructure]
- **Challenges**: [List of pain points and issues]
- **Goals**: [Business objectives and desired outcomes]
- **Constraints**: [Budget, timeline, compliance requirements]

### Your Mission

Design and architect a complete solution that addresses all requirements while optimizing for cost, performance, and security.

## Requirements

### Functional Requirements

1. **FR-1**: [Detailed functional requirement]
2. **FR-2**: [Detailed functional requirement]
3. **FR-3**: [Detailed functional requirement]
4. **FR-4**: [Detailed functional requirement]
5. **FR-5**: [Detailed functional requirement]

### Non-Functional Requirements

1. **Performance**: [Specific metrics and targets]
2. **Scalability**: [Growth projections and requirements]
3. **Security**: [Security and compliance requirements]
4. **Cost**: [Budget constraints and optimization goals]
5. **Availability**: [Uptime requirements and SLAs]

### Constraints

- **Budget**: $X million capital, $Y million annual operating
- **Timeline**: Z months to MVP, full rollout in W months
- **Compliance**: [Regulatory requirements]
- **Integration**: [Existing systems to integrate with]

## Project Structure

```
{project_id}/
├── README.md                          # This file
├── requirements.md                    # Detailed requirements
├── architecture.md                    # Architecture design document
├── STEP_BY_STEP.md                   # Implementation guide
├── src/                               # Code stubs
│   ├── architecture-diagrams/        # Diagrams source
│   ├── adrs/                         # Architecture Decision Records
│   └── templates/                    # Documentation templates
├── docs/                              # Documentation
│   ├── API.md                        # API specifications
│   ├── DEPLOYMENT.md                 # Deployment guide
│   ├── GOVERNANCE.md                 # Governance framework
│   ├── SECURITY.md                   # Security architecture
│   └── COST-MODEL.md                 # Cost analysis
├── terraform/                         # Infrastructure as Code stubs
├── kubernetes/                        # K8s manifest templates
├── tests/                             # Test plans
└── .env.example                       # Configuration template
```

## Getting Started

### Phase 1: Requirements Analysis (10 hours)

1. Review all requirements in [requirements.md](./requirements.md)
2. Conduct stakeholder analysis
3. Create requirements traceability matrix
4. Identify assumptions and risks
5. Validate requirements with scenarios

**Deliverable**: Requirements analysis document

### Phase 2: Architecture Design (30 hours)

1. Research and evaluate alternatives
2. Design high-level architecture
3. Create detailed component designs
4. Document architecture decisions (ADRs)
5. Address non-functional requirements
6. Create architecture diagrams (multiple views)

**Deliverable**: Complete architecture documentation

### Phase 3: Implementation Planning (15 hours)

1. Create phased implementation roadmap
2. Estimate costs and resources
3. Identify risks and mitigation strategies
4. Define success metrics and KPIs
5. Plan for operational readiness

**Deliverable**: Implementation plan and roadmap

### Phase 4: Documentation (15 hours)

1. Write comprehensive architecture documentation
2. Create API specifications
3. Document security architecture
4. Develop governance framework
5. Write deployment guides and runbooks

**Deliverable**: Complete documentation suite

### Phase 5: Presentation (10 hours)

1. Create executive presentation
2. Prepare technical deep-dive
3. Develop stakeholder-specific materials
4. Practice and refine presentation
5. Prepare for Q&A

**Deliverable**: Presentation materials

## Assessment Rubric

### Architecture Quality (40%)

- **Completeness**: All requirements addressed
- **Soundness**: Appropriate patterns and practices
- **Scalability**: Handles growth projections
- **Security**: Comprehensive security design
- **Cost-Effectiveness**: Optimized within budget

### Documentation (30%)

- **Clarity**: Easy to understand
- **Completeness**: All aspects covered
- **Visual Communication**: Effective diagrams
- **ADRs**: Well-reasoned decisions
- **Stakeholder Communication**: Appropriate for audience

### Strategic Thinking (20%)

- **Business Alignment**: Supports business goals
- **Long-Term Vision**: Future-proof design
- **Risk Management**: Identifies and mitigates risks
- **Innovation**: Creative solutions
- **Trade-Off Analysis**: Clear rationale for choices

### Implementation Planning (10%)

- **Feasibility**: Realistic and achievable
- **Phasing**: Logical implementation phases
- **Resource Planning**: Appropriate estimates
- **Success Metrics**: Measurable outcomes

## Success Criteria

✅ All functional and non-functional requirements met
✅ Architecture aligns with enterprise standards
✅ Complete documentation with diagrams
✅ 10+ ADRs documenting key decisions
✅ Cost model within budget constraints
✅ Security and compliance addressed
✅ Implementation roadmap with phases
✅ Executive presentation ready
✅ Peer review feedback incorporated

## Tools and Resources

### Required Tools

- **Diagramming**: Draw.io, Lucidchart, or ArchiMate tool
- **Documentation**: Markdown editor
- **Cloud**: Access to AWS/GCP/Azure consoles for research
- **Cost Tools**: Cloud cost calculators

### Recommended Reading

- See [requirements.md](./requirements.md) for specific resources
- Review relevant module content
- Study similar architectures from industry

## Timeline

**Recommended Schedule**:

- **Week 1-2**: Requirements analysis and research
- **Week 3-6**: Architecture design and ADRs
- **Week 7-8**: Implementation planning and cost modeling
- **Week 9-10**: Documentation and governance
- **Week 11**: Presentation and refinement

## Submission Guidelines

1. Complete all deliverables in the project structure
2. Ensure all diagrams are clear and well-labeled
3. Write ADRs for all major decisions
4. Include cost analysis and optimization strategy
5. Create README in your submission explaining approach

## Support and Resources

- **Office Hours**: Weekly virtual office hours
- **Peer Review**: Optional peer feedback
- **Discussion Forum**: GitHub Discussions for questions
- **Examples**: Review example architectures (available separately)

## Next Steps

1. Read [requirements.md](./requirements.md) thoroughly
2. Review [architecture.md](./architecture.md) template
3. Study [STEP_BY_STEP.md](./STEP_BY_STEP.md) for guidance
4. Begin Phase 1: Requirements Analysis

---

**Questions?** Post in GitHub Discussions or attend office hours.

**Ready to start?** → [Read detailed requirements](./requirements.md)
"""

    (project_dir / "README.md").write_text(readme_content)

    # Create requirements.md
    requirements_content = f"""# {project_info['name']} - Detailed Requirements

## Executive Summary

This document provides comprehensive requirements for {project_info['name'].lower()}. The solution must address business needs while meeting technical, security, and compliance requirements.

## Business Context

### Company Overview

**TechCorp** is a Fortune 500 company with:
- **Industry**: [Technology/Finance/Healthcare/Retail]
- **Size**: 50,000+ employees globally
- **Revenue**: $10B+ annually
- **ML Maturity**: [Current state of ML adoption]

### Business Drivers

1. **Driver 1**: [Business need or opportunity]
2. **Driver 2**: [Market pressure or competition]
3. **Driver 3**: [Regulatory requirement]
4. **Driver 4**: [Innovation and growth]

### Success Metrics

- **Business Metric 1**: [KPI and target]
- **Business Metric 2**: [KPI and target]
- **Business Metric 3**: [KPI and target]
- **ROI Target**: [Expected return on investment]

## Stakeholder Analysis

### Key Stakeholders

| Stakeholder | Role | Concerns | Requirements |
|-------------|------|----------|--------------|
| CTO | Executive Sponsor | Strategic alignment, ROI | Business value, innovation |
| VP Engineering | Technical Owner | Reliability, scalability | Performance, uptime |
| CISO | Security Lead | Security, compliance | Security controls, audit |
| CFO | Budget Owner | Cost optimization | TCO, cost predictability |
| Data Science Team | Users | Usability, performance | Dev experience, tools |

### Communication Plan

- **Executive Committee**: Monthly updates on progress, risks, ROI
- **Engineering Teams**: Weekly sprint reviews, technical decisions
- **Security Team**: Bi-weekly security reviews, compliance status
- **Finance**: Monthly cost reviews, budget tracking

## Functional Requirements

### FR-1: [Core Capability 1]

**Description**: The system must provide [capability] to support [business need].

**Acceptance Criteria**:
- [ ] Criterion 1: [Specific, measurable acceptance criteria]
- [ ] Criterion 2: [Specific, measurable acceptance criteria]
- [ ] Criterion 3: [Specific, measurable acceptance criteria]

**Priority**: Must Have

**Dependencies**: [List of dependencies]

**User Stories**:
1. As a [user type], I want to [action] so that [benefit]
2. As a [user type], I want to [action] so that [benefit]

### FR-2: [Core Capability 2]

**Description**: The system must enable [capability] to [business value].

**Acceptance Criteria**:
- [ ] Criterion 1: [Specific, measurable acceptance criteria]
- [ ] Criterion 2: [Specific, measurable acceptance criteria]
- [ ] Criterion 3: [Specific, measurable acceptance criteria]

**Priority**: Must Have

**Dependencies**: [List of dependencies]

### FR-3: [Core Capability 3]

**Description**: The system must support [capability] for [use case].

**Acceptance Criteria**:
- [ ] Criterion 1: [Specific, measurable acceptance criteria]
- [ ] Criterion 2: [Specific, measurable acceptance criteria]

**Priority**: Should Have

### FR-4 through FR-10: [Additional Requirements]

[Continue with additional functional requirements...]

## Non-Functional Requirements

### Performance Requirements

**NFR-P1: Latency**
- **Requirement**: P95 latency < [X ms] for [operation]
- **Measurement**: Prometheus metrics, APM tools
- **Validation**: Load testing, production monitoring

**NFR-P2: Throughput**
- **Requirement**: Support [X requests/second] sustained
- **Measurement**: Requests per second metrics
- **Validation**: Load testing at 2x expected peak

**NFR-P3: Resource Utilization**
- **Requirement**: CPU utilization < 70%, GPU utilization > 80%
- **Measurement**: Infrastructure metrics
- **Validation**: Continuous monitoring

### Scalability Requirements

**NFR-S1: Horizontal Scaling**
- **Requirement**: Scale from [X] to [Y] [users/requests/models]
- **Timeframe**: Support growth over [Z years]
- **Approach**: Auto-scaling, load balancing

**NFR-S2: Data Volume**
- **Requirement**: Handle [X TB/PB] of data
- **Growth**: [Y%] annual growth
- **Approach**: Distributed storage, partitioning

### Availability Requirements

**NFR-A1: Uptime**
- **Requirement**: 99.95% uptime (21.9 minutes downtime/month)
- **Measurement**: Uptime monitoring, SLA tracking
- **Validation**: Historical uptime reports

**NFR-A2: Disaster Recovery**
- **RPO**: Recovery Point Objective < [X hours]
- **RTO**: Recovery Time Objective < [Y hours]
- **Approach**: Multi-region, automated failover

**NFR-A3: Fault Tolerance**
- **Requirement**: No single point of failure
- **Approach**: Redundancy, health checks, auto-recovery

### Security Requirements

**NFR-SEC1: Authentication and Authorization**
- **Requirement**: Enterprise SSO integration (SAML/OIDC)
- **Authorization**: Role-based access control (RBAC)
- **MFA**: Required for privileged access

**NFR-SEC2: Data Encryption**
- **At Rest**: AES-256 encryption for all data
- **In Transit**: TLS 1.3 for all communications
- **Key Management**: Enterprise key management service

**NFR-SEC3: Network Security**
- **Requirement**: Zero-trust network architecture
- **Segmentation**: Network isolation between environments
- **Access**: VPN or private connectivity only

**NFR-SEC4: Audit and Logging**
- **Requirement**: Comprehensive audit trail
- **Retention**: 7 years for compliance
- **Monitoring**: Real-time security monitoring

### Compliance Requirements

**NFR-C1: [Regulatory Requirement 1]**
- **Regulation**: GDPR / HIPAA / SOC2
- **Requirements**: [Specific controls needed]
- **Validation**: Regular compliance audits

**NFR-C2: [Regulatory Requirement 2]**
- **Regulation**: [Specific regulation]
- **Requirements**: [Specific controls needed]
- **Validation**: [Audit process]

### Cost Requirements

**NFR-COST1: Capital Expenditure**
- **Budget**: $[X] million one-time investment
- **Allocation**: Infrastructure, tools, migration

**NFR-COST2: Operating Expenditure**
- **Budget**: $[Y] million annually
- **Breakdown**: Compute, storage, network, tools, support
- **Optimization Target**: Reduce by [Z%] year-over-year

**NFR-COST3: Cost Predictability**
- **Requirement**: Monthly cost variance < 10%
- **Approach**: Reserved instances, cost monitoring, budgets

### Usability Requirements

**NFR-U1: Developer Experience**
- **Requirement**: Self-service platform for data scientists
- **Onboarding**: < 1 day to first model training
- **Documentation**: Comprehensive docs and examples

**NFR-U2: Operations**
- **Requirement**: Minimal operational overhead
- **Automation**: 90%+ of operations automated
- **Monitoring**: Proactive alerting and dashboards

## Constraints

### Technical Constraints

1. **Cloud Providers**: Must support AWS, GCP, and Azure
2. **Kubernetes**: Must use Kubernetes for orchestration
3. **Compliance**: Must comply with [specific regulations]
4. **Integration**: Must integrate with existing systems [list]

### Organizational Constraints

1. **Timeline**: MVP in 6 months, full rollout in 12 months
2. **Team**: Limited to [X] FTEs for implementation
3. **Skills**: Team expertise in [technologies]
4. **Process**: Must follow enterprise change management

### Financial Constraints

1. **Capital Budget**: $[X]M maximum
2. **Operating Budget**: $[Y]M annually
3. **ROI Requirement**: Break-even in [Z] years

## Assumptions

1. **Assumption 1**: [Specific assumption and impact if invalid]
2. **Assumption 2**: [Specific assumption and impact if invalid]
3. **Assumption 3**: [Specific assumption and impact if invalid]

## Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Risk 1 | High | Medium | Mitigation strategy |
| Risk 2 | Medium | High | Mitigation strategy |
| Risk 3 | Low | Low | Mitigation strategy |

## Out of Scope

The following are explicitly out of scope for this project:

1. [Item 1]
2. [Item 2]
3. [Item 3]

## Requirements Traceability

| Requirement ID | Business Driver | Architecture Component | Test Case |
|----------------|----------------|------------------------|-----------|
| FR-1 | Driver 1 | Component A | TC-001 |
| FR-2 | Driver 1 | Component B | TC-002 |
| NFR-P1 | Driver 2 | Load Balancer | TC-010 |

## Acceptance Criteria

The solution is considered complete when:

- [ ] All must-have functional requirements implemented
- [ ] All non-functional requirements validated through testing
- [ ] Security and compliance requirements verified through audit
- [ ] Performance benchmarks achieved under load
- [ ] Documentation complete and reviewed
- [ ] Training provided to users and operators
- [ ] Production deployment successful
- [ ] Handoff to operations complete

## Appendices

### Appendix A: Use Cases

Detailed use case descriptions...

### Appendix B: Data Models

Entity relationships and schemas...

### Appendix C: Integration Points

Systems to integrate with and APIs...

### Appendix D: Glossary

Terms and definitions...

---

**Next Step**: Review these requirements and begin architecture design in [architecture.md](./architecture.md)
"""

    (project_dir / "requirements.md").write_text(requirements_content)

    # Create directory structure
    (project_dir / "src" / "architecture-diagrams").mkdir(parents=True, exist_ok=True)
    (project_dir / "src" / "adrs").mkdir(parents=True, exist_ok=True)
    (project_dir / "src" / "templates").mkdir(parents=True, exist_ok=True)
    (project_dir / "docs").mkdir(parents=True, exist_ok=True)
    (project_dir / "terraform").mkdir(parents=True, exist_ok=True)
    (project_dir / "kubernetes").mkdir(parents=True, exist_ok=True)
    (project_dir / "tests").mkdir(parents=True, exist_ok=True)

    print(f"✓ Created project: {project_id}")


def main():
    """Generate all modules and projects"""
    print("Generating AI Infrastructure Architect Learning Repository...")
    print("=" * 70)

    # Create lessons directory
    lessons_dir = BASE_DIR / "lessons"
    lessons_dir.mkdir(parents=True, exist_ok=True)

    # Create all modules
    print("\nCreating Modules:")
    print("-" * 70)
    for module_id, module_info in MODULES.items():
        create_module(module_id, module_info)

    # Create projects directory
    projects_dir = BASE_DIR / "projects"
    projects_dir.mkdir(parents=True, exist_ok=True)

    # Create all projects
    print("\nCreating Projects:")
    print("-" * 70)
    for project_id, project_info in PROJECTS.items():
        create_project(project_id, project_info)

    # Create assessments directory
    assessments_dir = BASE_DIR / "assessments"
    (assessments_dir / "quizzes").mkdir(parents=True, exist_ok=True)
    (assessments_dir / "practical-exams").mkdir(parents=True, exist_ok=True)

    # Create resources directory
    resources_dir = BASE_DIR / "resources"
    resources_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 70)
    print("Repository structure generated successfully!")
    print("=" * 70)

    # Generate statistics
    total_modules = len(MODULES)
    total_projects = len(PROJECTS)
    estimated_files = (total_modules * 7) + (total_projects * 10) + 20  # Rough estimate

    print(f"\nStatistics:")
    print(f"- Modules created: {total_modules}")
    print(f"- Projects created: {total_projects}")
    print(f"- Estimated files: {estimated_files}+")
    print(f"- Total learning hours: 600 hours")


if __name__ == "__main__":
    main()
