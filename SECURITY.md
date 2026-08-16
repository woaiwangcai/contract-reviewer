# Security

## Data handling

Contract text is sent to the HTTPS API endpoint configured in `MODEL_BASE_URL`. Before
using the project with confidential material, confirm the provider's storage,
retention, training, and data-transfer policies.

The project does not cache model responses. Generated reports are written only to the
selected local output directory.

## Secrets

Store API credentials in `.env`. The file is excluded by `.gitignore`. Never commit
real API keys, confidential contracts, generated reports, or request logs.

## Reporting a vulnerability

Do not open a public issue containing a secret or confidential contract. Submit a
private report through [GitHub Security Advisories](https://github.com/woaiwangcai/contract-reviewer/security/advisories/new).
