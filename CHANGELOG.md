# Changelog

All notable changes to FastPatch are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added (beta)
- **Auto-rollback for Windows:** baseline before the patch, health check after the restart window (services that ran before, required services, crash events). If the machine is unhealthy, only the new update is removed, staged with no restart, and reported as rolled back only after a restart proves it's gone. One attempt per update; servicing stack updates go to an engineer.
- **macOS patching:** Apple updates through `softwareupdate` with disk, battery and catalog checks. No-restart updates install now; restart-required updates install on Intel and download for MDM or user approval on Apple silicon. Verify confirms each update is no longer offered. Never restarts a Mac.
- New outcome label: **Rolled back**.

### Planned
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
