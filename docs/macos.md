# macOS patching (new, beta)

FastPatch now patches Macs through Apple's own `softwareupdate` tool, run by the Kaseya agent. Same loop, same guardrails, same outcome labels as Windows.

## The loop on a Mac

| Stage | What happens |
|---|---|
| **Check** | Free space on the data volume, battery level when unplugged, and that Apple's update catalog is reachable |
| **Scan** | One scan for available updates per run |
| **Apply** | Each update is handled by type (below) and tried once per run |
| **Verify** | After your restart window, an update counts as done only when Apple no longer offers it |
| **Report** | One ticket-ready line: outcome, cause and action |

## How each update is handled

| Update type | What FastPatch does | Outcome |
|---|---|---|
| No restart needed (Safari, security data, command line tools) | Installs it now | Fixed itself |
| Restart needed, Intel Mac | Installs it; it completes in your restart window | Waiting for a restart |
| Restart needed, Apple silicon Mac | Downloads it; Apple requires a user or MDM to authorise the install | Needs a decision |

## When it waits or hands over

| Situation | Outcome |
|---|---|
| Laptop unplugged and battery low | Try again later |
| Apple's update catalog unreachable | Try again later |
| Not enough free disk space | Needs an engineer |
| An update failed to install | Needs an engineer, and it isn't retried blindly on the next run |
| An update is still offered after it was installed | Needs an engineer |

## Guardrails

- Never restarts a Mac.
- Never changes Software Update settings, deferrals or ignored updates.
- One scan per run, and each update is tried at most once per run.
- Never reports success without proof: verify checks the update is no longer offered.

## Limits in this beta

- No rollback on Mac: Apple doesn't support removing installed macOS updates.
- On Apple silicon, restart-required updates need a user or MDM to authorise them. FastPatch downloads them so the install is quick once approved.
