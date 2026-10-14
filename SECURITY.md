# Security policy

## Reporting a vulnerability

Please report security issues privately by email to **[rehank9540@gmail.com](mailto:rehank9540@gmail.com?subject=FastPatch%20security%20report)**. Do not open a public issue.

Include what you found, how to reproduce it and the impact you expect. You will get an acknowledgement, and fixes are released through the normal approval process before reaching production.

## Supported versions

| Version | Supported |
|---|---|
| 5.1.x | ✅ |
| Older | ❌ |

## Security by design

- No new software on endpoints: FastPatch runs through the existing Kaseya agent as a signed procedure.
- No restarts, no update-policy changes and no changes to antivirus or security tools. See [docs/guardrails.md](docs/guardrails.md).
- Every production release is approved by a person.
