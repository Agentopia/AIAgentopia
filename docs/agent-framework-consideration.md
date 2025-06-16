# AIAgentopia: Agent Framework Strategy

## Purpose
This document outlines the strategy for using multiple agent frameworks within the AIAgentopia repository while maintaining development efficiency and system stability.

## Framework Selection Criteria

### Primary Considerations
- **Maturity & Maintenance**: Actively maintained with regular updates
- **Community Support**: Strong community and documentation
- **License**: Compatible with MIT License
- **Performance**: Efficient resource usage
- **Extensibility**: Ability to customize and extend functionality

### Secondary Considerations
- Learning curve for the team
- Integration capabilities with other tools
- Deployment complexity
- Monitoring and debugging support

## Approved Frameworks

| Framework | Best For | Version | Notes |
|-----------|----------|---------|-------|
| LangChain | General-purpose agents | ≥0.0.200 | Good documentation, active community |
| AutoGen | Multi-agent conversations | ≥0.2.0 | Microsoft-backed, good for collaborative agents |
| Haystack | NLP-focused agents | ≥1.15.0 | Strong document processing capabilities |
| Custom | Specialized requirements | - | When existing frameworks don't fit |

## Directory Structure

```
/agents/
  {agent-name}/
    app/                     # Core source code
    tests/                   # Agent-specific tests
    docs/                    # Agent-specific detailed documentation
    .env.example             # Example environment variables file
    agent.json               # Agent manifest file
    Dockerfile               # Docker configuration for deployment
    requirements.txt         # Python dependencies
    README.md                # Agent overview, setup, usage
```

## Dependency Management

### Virtual Environments
Each agent must include:
- A `requirements.txt` with pinned versions
- A `setup.py` or `pyproject.toml` if the agent is installable

Example `requirements.txt`:
```
# Core dependencies
langchain==0.0.267
openai==0.27.8

# Dev dependencies
pytest==7.3.1
ruff==0.0.272
```

## Containerization Standards

### Base Images
- Use `python:3.10-slim` as the base image unless specific requirements dictate otherwise
- Multi-stage builds for production containers

### Container Requirements
- Non-root user
- Health checks
- Proper signal handling
- Resource limits

Example `Dockerfile`:
```dockerfile
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.10-slim
WORKDIR /app

# Copy only the necessary files
COPY --from=builder /root/.local /root/.local
COPY . .

# Ensure scripts in .local are usable
ENV PATH="/root/.local/bin:${PATH}"

# Run as non-root user
RUN useradd -m agent && \
    chown -R agent:agent /app
USER agent

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "app/main.py"]
```

## Development Workflow

### Adding a New Framework
1. **Proposal**: Create an issue detailing:
   - Framework benefits
   - Use cases
   - Maintenance status
   - Integration plan

2. **Approval**: Requires review from at least two maintainers

3. **Implementation**:
   - Add to approved frameworks list
   - Create a template in `/templates/frameworks/{framework-name}`
   - Update documentation

### Version Management
- Pin all dependencies
- Use Dependabot for security updates
- Regular dependency audits

## Common Services Integration

### Logging
Use the standard Python logging module with JSON formatting:

```python
import logging
import json_log_formatter

formatter = json_log_formatter.JSONFormatter()
json_handler = logging.StreamHandler()
json_handler.setFormatter(formatter)

logger = logging.getLogger('agent')
logger.addHandler(json_handler)
logger.setLevel(logging.INFO)
```

### Monitoring
- Expose Prometheus metrics endpoint
- Standard metrics:
  - Request count
  - Request duration
  - Error rates
  - Resource usage

## Testing Strategy

### Required Test Types
1. **Unit Tests**: Test individual components
2. **Integration Tests**: Test framework integration
3. **Performance Tests**: Benchmark critical paths
4. **Security Scans**: Dependency and code analysis

### CI/CD Integration
- Run tests in isolated environments
- Performance regression testing
- Security scanning
- Container vulnerability scanning

## Documentation Standards

Each agent must include:
- `README.md` with:
  - Purpose and features
  - Setup instructions
  - Configuration options
  - API documentation
  - Examples

## Security Considerations

### Required Practices
- No secrets in code
- Regular dependency updates
- Security headers for web services
- Input validation
- Output encoding
- Rate limiting

## Performance Guidelines

### Resource Limits
- Set memory limits in Docker
- Configure timeouts
- Implement circuit breakers
- Use connection pooling

### Caching
- Cache frequent operations
- Invalidate cache appropriately
- Consider distributed caching for multi-instance deployments

## Framework-Specific Guidelines

### LangChain
- Use LCEL (LangChain Expression Language) for complex chains
- Implement proper error handling for LLM calls
- Cache LLM responses when appropriate

### AutoGen
- Document agent roles and responsibilities
- Implement conversation logging
- Set message size limits

## Review Process

### Quarterly Reviews
- Assess framework usage
- Check for better alternatives
- Update dependencies
- Review performance metrics

### Deprecation Policy
- 3-month notice for breaking changes
- Migration guides for major updates
- Archive deprecated agents in a separate branch

---

*Last Updated: June 13, 2025*
*Version: 1.0.0*
