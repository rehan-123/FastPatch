# Changelog

All notable changes to FastPatch are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Planned
- macOS support (next build)
- Reboot proof
- Central result collection
- Health checks

## [5.1.0] – current production release

### Live
- Six-stage loop on every machine: detect, diagnose, classify, remediate, verify, report
- Five timestamped checks: component store, pending reboot, servicing stack, update error code, system volume
- Approved fix per cause, inside the client's approval policy, rolled out one machine group at a time
- Verification that the update is installed after the restart
- Ticket-ready result line per machine and five outcome labels
- Guardrails: no restarts, no update-policy changes, no deleting repair files, no changes to security tools, bounded runs
- 600+ machines patched in production at a 99% success rate
