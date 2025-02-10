# GitHub Self-hosted Runner Connectivity Checker

A Python tool for checking network connectivity of GitHub Actions self-hosted runners. It helps you quickly verify if your self-hosted runner can access all required GitHub domains.

## Use Cases

This tool is particularly useful when deploying GitHub Actions self-hosted runners in:
- Corporate network environments
- Networks with firewall restrictions
- Proxy server environments
- Networks with special routing policies

## Features

- 🔍 Comprehensive connectivity check for all required domains
- 📊 Results displayed by functional categories
- 🎨 Clear tabulated output with color-coded status
- ⚡ Concurrent checking for efficiency
- 🛡️ Smart HTTP response validation
- 💾 JSON output for further processing

## Requirements

- Python 3.6+
- Required packages (installed via pip):
  - requests>=2.31.0
  - prettytable>=3.9.0
  - colorama>=0.4.6

## Installation

1. Clone the repository:
```bash
git clone https://github.com/super-ultraman/gitHub-runner-connectivity-checker
cd gitHub-runner-connectivity-checker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

1. Run the checker:
```bash
python github-runner-checker.py
```

2. Check the output:
   - The results will be displayed in a colored table in your terminal
   - A JSON file with detailed results will be saved as `domain_check_results_[timestamp].json`

## Output Format

The tool provides two types of output:

1. Console Output:
   - Real-time formatted table display
   - Color-coded status indicators (✓ for success, ✗ for failure)
   - Detailed connection information including IP addresses and HTTP status codes

2. JSON Output:
   - Detailed results saved in `domain_check_results_[timestamp].json`
   - Includes complete check data for each domain
   - Suitable for automated processing or integration with other tools

## Domain Categories

The checked domains are based on GitHub's official documentation: [About self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)

Categories include:
- Essential Operations
- Downloading Actions
- GitHub Packages & Publishing Actions
- Artifacts and Logs
- Runner Updates
- OIDC Tokens
- Git LFS
- Dependabot

## Status Definitions

- ✓ Normal:
  - HTTP status codes 200-399
  - HTTP status codes 400/403/404/405 (indicating permission or resource issues, not connectivity problems)
- ✗ Abnormal:
  - HTTP 5xx status codes
  - DNS resolution failures
  - Connection timeouts

## Common Issues

Permission-related status codes (like 403, 404) are considered normal as they indicate the network is accessible but the resource either requires authentication or doesn't exist.

## Contributing

Issues and Pull Requests are welcome to improve this tool. When submitting PRs, please ensure:
- Code follows Python PEP 8 standards
- Necessary comments and documentation are included
- All tests pass
