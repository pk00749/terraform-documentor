# Development Guide

This document provides comprehensive guidance for generating and maintaining Terraform module documentation. It serves different audiences with specific workflows and best practices.

## Target Audiences

This documentation helps:

- **New Developers** - Quickly understand project structure and usage
- **Maintainers** - Daily maintenance and troubleshooting
- **CI/CD Engineers** - Integration into automated pipelines
- **Module Developers** - Standard process for adding new modules

## Prerequisites

Before using the documentation generation system, ensure you have:

1. **Python 3.7+** installed
2. **terraform-docs** installed ([Installation Guide](https://terraform-docs.io/user-guide/installation/))
3. **Terraform** environment configured
4. **Make** utility (optional, but recommended)

## Project Structure

```
terraform-documentor/
├── config/
│   ├── english-docs.yml    # English documentation configuration
│   └── chinese-docs.yml    # Chinese documentation configuration
├── modules/
│   ├── ec2/               # EC2 module
│   ├── rds/               # RDS module
│   ├── s3/                # S3 module
│   ├── security-group/    # Security Group module
│   └── vpc/               # VPC module
├── generate-docs.py       # Python documentation generator
├── Makefile              # Build automation
└── README.md             # Project overview
```

## Quick Start

### Using Make (Recommended)

```bash
# Show available commands
make help

# Generate English documentation for all modules
make docs-en

# Generate Chinese documentation for all modules
make docs-cn

# Generate documentation in both languages
make docs

# Check dependencies
make check-deps

# Clean temporary files
make clean
```

### Using Python Script Directly

```bash
# Generate English documentation
python3 generate-docs.py english

# Generate Chinese documentation
python3 generate-docs.py chinese

# Generate both languages
python3 generate-docs.py all
```

## Configuration Files

The system uses centralized configuration files located in the `config/` directory:

### english-docs.yml
- English documentation templates
- Standard terraform-docs configuration
- Includes "Notes" section with environment requirements

### chinese-docs.yml
- Chinese documentation templates
- Localized section headers (环境要求, 输入变量, etc.)
- Same structure as English version

## For New Developers

### Getting Started
1. Clone the repository
2. Install dependencies: `make check-deps`
3. Generate documentation: `make docs`
4. Review generated README.md files in each module

### Understanding the System
- Each module must have a `main.tf` file to be recognized
- Documentation is generated from Terraform comments and metadata
- Configuration is centralized but applied per-module
- Output is written to each module's README.md

## For Maintainers

### Daily Operations

#### Adding New Modules
1. Create module directory under `modules/`
2. Add required Terraform files (`main.tf`, `variables.tf`, `outputs.tf`)
3. Run documentation generation: `make docs`
4. Verify generated README.md

#### Updating Documentation
1. Modify Terraform files with proper comments
2. Update configuration files if needed
3. Regenerate documentation: `make docs`
4. Review changes in README.md files

#### Troubleshooting

**Common Issues:**

1. **terraform-docs not found**
   ```bash
   # Install terraform-docs
   # macOS
   brew install terraform-docs

   # Linux
   curl -sSLo ./terraform-docs.tar.gz https://terraform-docs.io/dl/v0.16.0/terraform-docs-v0.16.0-$(uname)-amd64.tar.gz
   tar -xzf terraform-docs.tar.gz
   chmod +x terraform-docs
   mv terraform-docs /usr/local/bin/
   ```

2. **Module not found**
   - Ensure module directory contains `main.tf`
   - Check module path in `modules/` directory

3. **Configuration errors**
   - Validate YAML syntax in config files
   - Check file permissions

4. **Documentation not updating**
   - Clear temporary files: `make clean`
   - Regenerate: `make docs`

### Maintenance Schedule
- **Weekly**: Review and update module documentation
- **Monthly**: Update configuration templates if needed
- **On new releases**: Regenerate all documentation

## For CI/CD Engineers

### Pipeline Integration

#### GitHub Actions Example
```yaml
name: Update Documentation
on:
  push:
    paths:
      - 'modules/**/*.tf'
  pull_request:
    paths:
      - 'modules/**/*.tf'

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install terraform-docs
        run: |
          curl -sSLo ./terraform-docs.tar.gz https://terraform-docs.io/dl/v0.16.0/terraform-docs-v0.16.0-linux-amd64.tar.gz
          tar -xzf terraform-docs.tar.gz
          chmod +x terraform-docs
          sudo mv terraform-docs /usr/local/bin/
      - name: Generate documentation
        run: make docs
      - name: Check for changes
        run: git diff --exit-code || (echo "Documentation needs updating" && exit 1)
```

#### Jenkins Pipeline Example
```groovy
pipeline {
    agent any
    stages {
        stage('Check Dependencies') {
            steps {
                sh 'make check-deps'
            }
        }
        stage('Generate Documentation') {
            steps {
                sh 'make docs'
            }
        }
        stage('Commit Changes') {
            when {
                changeset "modules/**/*.tf"
            }
            steps {
                sh '''
                    git config user.name "Jenkins"
                    git config user.email "jenkins@company.com"
                    git add modules/*/README.md
                    git commit -m "Update module documentation [skip ci]" || true
                    git push origin main
                '''
            }
        }
    }
}
```

### Automation Best Practices
- Run documentation generation on every Terraform file change
- Include documentation validation in PR checks
- Auto-commit documentation updates
- Set up notifications for failed documentation builds

## For Module Developers

### Standard Module Structure
```
modules/your-module/
├── main.tf          # Required: Main resource definitions
├── variables.tf     # Required: Input variables
├── outputs.tf       # Required: Output values
├── versions.tf      # Optional: Provider requirements
└── README.md        # Generated: Do not edit manually
```

### Documentation Best Practices

#### Variable Documentation
```hcl
variable "instance_type" {
  description = "The type of instance to start"
  type        = string
  default     = "t3.micro"

  validation {
    condition     = can(regex("^t[23]\\.", var.instance_type))
    error_message = "Instance type must be a t2 or t3 instance."
  }
}
```

#### Output Documentation
```hcl
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.this.id
}

output "public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.this.public_ip
  sensitive   = false
}
```

#### Resource Documentation
```hcl
# Create EC2 instance with specified configuration
resource "aws_instance" "this" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = {
    Name        = var.instance_name
    Environment = var.environment
  }
}
```

### Module Development Workflow
1. Create module directory structure
2. Implement Terraform resources with proper comments
3. Define input variables with descriptions
4. Define outputs with descriptions
5. Test module functionality
6. Generate documentation: `make docs`
7. Review generated README.md
8. Create pull request

### Quality Guidelines
- All variables must have descriptions
- All outputs must have descriptions
- Use meaningful variable names
- Include validation rules where appropriate
- Add examples in module comments
- Follow Terraform best practices

## Advanced Usage

### Custom Configuration
You can modify the configuration files to customize:
- Section order and visibility
- Output format and styling
- Template content
- File output locations

### Script Customization
The Python script supports:
- Custom module directories
- Custom configuration directories
- Batch processing
- Error handling and reporting

### Integration with Other Tools
- **Pre-commit hooks**: Automatically generate docs before commits
- **IDE plugins**: Integrate with editor workflows
- **Documentation sites**: Export to documentation platforms

## Support and Resources

- **terraform-docs**: https://terraform-docs.io/
- **Terraform Documentation**: https://www.terraform.io/docs/
- **Project Issues**: Check the repository's issue tracker
- **Contributing**: Follow the project's contribution guidelines

---

*This guide is maintained as part of the Terraform documentation system. Updates should be made through the standard development workflow.*
