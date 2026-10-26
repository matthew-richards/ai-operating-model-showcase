# Security policy

This repository contains documentation and diagrams only. It holds no credentials, infrastructure details, or production code.

## Reporting

If you find something here that looks sensitive, such as a credential, hostname, or personal detail, please report it privately through GitHub's "Report a vulnerability" option on the Security tab instead of opening a public issue.

## Controls on this repository

- Every pull request runs a secrets scan (gitleaks).
- The main branch requires the Definition-of-Done check, blocks force-push and deletion, and allows no bypass.
