# Security policy

This repository contains documentation and diagrams only. It holds no credentials, infrastructure details, or production code.

## Reporting

If you find something here that looks sensitive, such as a credential, hostname, or personal detail, please report it privately through GitHub's "Report a vulnerability" option on the Security tab instead of opening a public issue.

## Controls on this repository

- The main branch ruleset blocks force-push and deletion, with no bypass.
- GitHub secret scanning and push protection are on.
- CI checks (Definition of Done, gitleaks secrets scan, Markdown lint) run on every pull request and are required before merge. A Vale prose check runs as advice only.
