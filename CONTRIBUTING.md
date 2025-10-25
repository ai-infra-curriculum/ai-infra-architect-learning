# Contributing to AI Infrastructure Architect Learning

Thank you for your interest in contributing! This document provides guidelines for contributing to the AI Infrastructure Architect curriculum.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Types of Contributions](#types-of-contributions)
- [Contribution Guidelines](#contribution-guidelines)
- [Style Guidelines](#style-guidelines)
- [Review Process](#review-process)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## How to Contribute

### Reporting Issues

If you find an error, typo, or have a suggestion:

1. Check if the issue already exists in GitHub Issues
2. If not, create a new issue with:
   - Clear title describing the issue
   - Detailed description of the problem or suggestion
   - Location in the curriculum (module/project/section)
   - If reporting an error, include expected vs actual behavior
   - Screenshots if applicable

### Suggesting Enhancements

For feature requests or curriculum improvements:

1. Open a GitHub Issue with the enhancement label
2. Describe the enhancement and its value
3. Explain why it would be useful to learners
4. Provide examples if applicable

### Contributing Content

To contribute new content or improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Make your changes following the style guidelines
4. Test your changes (verify links, formatting, clarity)
5. Commit your changes with clear commit messages
6. Push to your fork
7. Open a Pull Request

## Types of Contributions

### Welcome Contributions

We especially welcome:

- **Typo and grammar fixes**: Help us maintain professional quality
- **Broken link fixes**: Keep resources accessible
- **Clarifications**: Make content easier to understand
- **New examples**: Real-world examples and case studies
- **Exercise improvements**: Better exercises or additional practice
- **Resource additions**: Relevant books, articles, tools
- **Diagram improvements**: Clearer architecture diagrams
- **Quiz questions**: Additional assessment questions

### Contributions Requiring Discussion

Please open an issue before working on:

- **New modules**: Discuss alignment with curriculum goals
- **Major restructuring**: Get consensus on approach
- **New projects**: Ensure they fit learning objectives
- **Curriculum sequence changes**: Maintain progressive learning
- **Assessment criteria changes**: Align with learning outcomes

## Contribution Guidelines

### Content Quality Standards

All contributions must meet these standards:

#### Accuracy
- Technical information must be correct and up-to-date
- Code examples must work as described
- Architecture patterns must follow best practices
- Cite sources for factual claims

#### Clarity
- Use clear, professional language
- Define technical terms on first use
- Provide context and examples
- Use active voice when possible

#### Completeness
- Include all necessary steps
- Don't assume prior knowledge beyond prerequisites
- Provide rationale for architectural decisions
- Include both what and why

#### Relevance
- Align with module learning objectives
- Support architect-level skill development
- Reflect current industry practices
- Provide practical value

### Module Content Guidelines

When contributing to modules:

#### Lecture Notes
- Use consistent heading structure (H1, H2, H3)
- Include diagrams for complex concepts
- Provide real-world examples
- Add case studies where relevant
- Link to authoritative sources

#### Exercises
- Clear learning objective for each exercise
- Realistic scenarios based on industry needs
- Step-by-step guidance
- Expected time to complete
- Evaluation criteria

#### Resources
- Prioritize high-quality, authoritative sources
- Include publication dates for time-sensitive content
- Verify all links work
- Provide brief descriptions of resources
- Organize by category

#### Quizzes
- Questions must assess stated learning objectives
- Provide clear, unambiguous answers
- Include explanations for correct answers
- Mix question types (MC, scenario-based, multiple select)
- Aim for 80% pass rate for prepared students

### Project Content Guidelines

When contributing to projects:

#### Architecture Documents
- Use standard architecture frameworks (TOGAF, C4)
- Include multiple viewpoints (business, application, technology)
- Document assumptions and constraints
- Explain trade-offs in decisions
- Provide scalability and security considerations

#### Code Stubs
- Include comprehensive TODO comments
- Provide clear guidance on implementation
- Follow language-specific style guides
- Include type hints and docstrings (Python)
- Add validation and error handling guidance

#### Documentation
- Write for diverse audiences (technical and business)
- Use consistent terminology
- Include troubleshooting sections
- Provide runbooks for operational tasks
- Add deployment and rollback procedures

## Style Guidelines

### Markdown Formatting

#### Headings
```markdown
# H1: Module or Document Title
## H2: Major Sections
### H3: Subsections
#### H4: Sub-subsections (use sparingly)
```

#### Lists
- Use `-` for unordered lists
- Use `1.` for ordered lists
- Indent sub-lists with 2 spaces

#### Code Blocks
```markdown
\`\`\`python
# Include language identifier
def example_function():
    """Include docstrings"""
    pass
\`\`\`
```

#### Links
```markdown
# Relative links for internal content
[Module 301](./lessons/mod-301-enterprise-architecture/)

# External links with descriptive text
[TOGAF Official Documentation](https://www.opengroup.org/togaf)
```

### Writing Style

#### Voice and Tone
- **Active voice**: "You design the architecture" (not "The architecture is designed")
- **Professional**: Maintain professional tone throughout
- **Encouraging**: Support learners' journey
- **Inclusive**: Use inclusive language (they/them when gender unknown)

#### Technical Terms
- **Define on first use**: "MLOps (Machine Learning Operations) is..."
- **Use consistently**: Don't alternate between synonyms
- **Provide context**: Explain why a term matters

#### Examples
- **Real-world**: Base examples on actual industry practices
- **Concrete**: Provide specific numbers and scenarios
- **Diverse**: Include examples from various industries

### Architecture Diagram Guidelines

#### Diagram Standards
- Use standard notation (UML, ArchiMate, C4 model)
- Include legend for symbols
- Keep diagrams focused (one concept per diagram)
- Use consistent colors and shapes
- Label all components clearly

#### Diagram Types
- **Context diagrams**: System boundaries and external actors
- **Container diagrams**: High-level technology choices
- **Component diagrams**: Internal structure
- **Deployment diagrams**: Infrastructure and deployment
- **Sequence diagrams**: Interactions over time

#### Tools
- Prefer editable formats (draw.io XML, PlantUML, Mermaid)
- Include source files in `/src/diagrams/`
- Export to PNG or SVG for documentation
- Use consistent styling across diagrams

### Code Style

#### Python
Follow PEP 8:
- 4 spaces for indentation
- 79 characters per line for code
- 72 characters per line for docstrings
- Type hints for functions
- Comprehensive docstrings

```python
def calculate_cost(
    instances: int,
    instance_type: str,
    hours: float
) -> float:
    """
    Calculate cloud infrastructure cost.

    Args:
        instances: Number of instances
        instance_type: Instance type (e.g., 't2.micro')
        hours: Runtime hours

    Returns:
        Total cost in USD
    """
    # Implementation with TODO comments
    pass
```

#### YAML/HCL (Infrastructure as Code)
- 2 spaces for indentation
- Comments explaining non-obvious configuration
- Consistent naming conventions
- Environment-specific variables

### Architecture Decision Records (ADRs)

Use this template for ADRs:

```markdown
# ADR-NNN: Title

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

### Positive
- Benefit 1
- Benefit 2

### Negative
- Trade-off 1
- Trade-off 2

### Risks
- Risk 1 and mitigation
- Risk 2 and mitigation

## Alternatives Considered
What other alternatives were considered?

### Alternative 1
- Description
- Pros
- Cons
- Why not chosen

## References
- Links to relevant documentation
- Related ADRs
```

## Review Process

### Pull Request Process

1. **Create PR**: Open a pull request with clear title and description
2. **Automated Checks**: CI will run automated validation
3. **Review Assignment**: Maintainer will review within 5 business days
4. **Feedback**: Address any feedback or requested changes
5. **Approval**: PR must be approved by at least one maintainer
6. **Merge**: Maintainer will merge when ready

### What Reviewers Look For

- **Correctness**: Technical accuracy
- **Clarity**: Easy to understand
- **Consistency**: Follows style guidelines
- **Completeness**: Includes all necessary information
- **Testing**: Links work, code runs, examples are valid
- **Value**: Provides clear value to learners

### Response Time

- **Issues**: Acknowledged within 3 business days
- **PRs**: Initial review within 5 business days
- **Questions**: Response within 2 business days

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes for significant contributions
- Acknowledged in documentation for substantial additions

## Questions?

- **General questions**: GitHub Discussions
- **Private concerns**: ai-infra-curriculum@joshua-ferguson.com
- **Bug reports**: GitHub Issues
- **Feature requests**: GitHub Issues with enhancement label

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers this project.

---

Thank you for helping make this curriculum better for everyone! 🚀
