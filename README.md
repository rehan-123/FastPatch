<div align="center">

<img src="assets/hero.svg" width="100%" alt="FastPatch: patch night, on autopilot. Self-healing Windows patch remediation for Kaseya VSA fleets. 600+ machines patched at 99% success. New: auto-rollback, and macOS patching in beta.">

<br>

<img src="https://img.shields.io/badge/status-live_in_production-3FD07A?style=for-the-badge&labelColor=0B1730" alt="Status: live in production">
<img src="https://img.shields.io/badge/platform-Kaseya_VSA-38C8F0?style=for-the-badge&labelColor=0B1730" alt="Platform: Kaseya VSA">
<img src="https://img.shields.io/badge/Windows-supported-38C8F0?style=for-the-badge&labelColor=0B1730&logo=windows&logoColor=white" alt="Windows supported">
<img src="https://img.shields.io/badge/macOS-beta-F5C451?style=for-the-badge&labelColor=0B1730&logo=apple&logoColor=white" alt="macOS beta">
<img src="https://img.shields.io/badge/new-auto--rollback-3FD07A?style=for-the-badge&labelColor=0B1730" alt="New: auto-rollback">
<img src="https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white&labelColor=0B1730" alt="PowerShell">

### Find every failed Windows update. Name the cause. Apply the approved fix. Prove it landed.

**[Features](#-features)** · **[Auto-rollback](#-new-auto-rollback)** · **[macOS](#-macos-patching-beta)** · **[How it runs](#-how-it-runs)** · **[Guardrails](#%EF%B8%8F-guardrails)** · **[Results](#-results-in-production)** · **[Roadmap](#%EF%B8%8F-roadmap)** · **[FAQ](#-faq)** · **[Get FastPatch](#-get-fastpatch)**

</div>

---

## 😩 The problem

Every MSP knows patch night. Kaseya says a few dozen machines failed. Someone exports them to a spreadsheet, logs into each one, guesses the cause, retries, and leaves a ticket note that only they can read. The next engineer starts from scratch.

**FastPatch moves that whole loop onto the Kaseya agent you already run.** Your engineers stop hunting for problems and start reading a short list of exceptions that already say what went wrong.

## ✨ Features

<img src="assets/features.svg" width="100%" alt="Features: diagnoses before it fixes; names the real cause; fixes inside your policy; proof, not job status; ticket-ready output; nothing new to install; auto-rollback (new); patches Macs too (beta); bounded by design.">

## 🆕 New: auto-rollback

<img src="assets/rollback.svg" width="100%" alt="Auto-rollback: baseline, patch, restart window, health check. Healthy means done. Unhealthy means the new update is removed with no restart forced, then proven gone after the next restart window, and you deny it in your approval policy.">

A patch that installs cleanly can still break a machine. FastPatch now takes a **baseline before the patch** and **checks the machine again after your restart window**. If something that worked before is broken, it removes only the update that just landed.

- 🩺 **Knows what "broken" means:** a service that ran before the patch is down, a service you marked as required is down, or Windows crashed since the patch
- 🎯 **Removes only the new update,** never anything that was already there
- 🔁 **Never forces a restart:** removal is staged and completes in your next restart window
- ✅ **Proves it:** "rolled back" only after a restart shows the update gone and the machine healthy
- 🧯 **Knows its limits:** one attempt per update; servicing stack updates can't be removed, so they go to an engineer
- 📝 **Closes the loop:** tells you which KB to deny in your approval policy, without touching your update settings itself

More in [docs/auto-rollback.md](docs/auto-rollback.md).

## 🍎 macOS patching (beta)

FastPatch now patches Macs through Apple's own `softwareupdate`, with the same loop, guardrails and outcome labels as Windows.

| Update type | What FastPatch does | Outcome |
|---|---|---|
| No restart needed (Safari, security data, tools) | Installs it now | ✅ Fixed itself |
| Restart needed, **Intel** Mac | Installs it; it completes in your restart window | ⏳ Waiting for a restart |
| Restart needed, **Apple silicon** Mac | Downloads it; Apple requires a user or MDM to authorise the install | 🔀 Needs a decision |

Before touching anything it checks free disk space, battery (it waits if a laptop is low and unplugged) and that Apple's update catalog is reachable. It never restarts a Mac and never changes Software Update settings. More in [docs/macos.md](docs/macos.md).

## 🔁 How it runs

<img src="assets/loop.svg" width="100%" alt="The run loop inside Kaseya VSA: schedule, run on the agent, result line, branch and log, verify.">

| Step | What happens |
|:-:|---|
| **01 · Schedule** | Kaseya runs a signed procedure for one machine group at a time |
| **02 · Run on the agent** | Five checks, then the approved fix for whatever they find |
| **03 · Result line** | Each machine reports its status, the cause and the action taken |
| **04 · Branch and log** | Kaseya routes every result by status and keeps the logs |
| **05 · Verify** | After your normal restart window, FastPatch confirms the update really installed |

### 🩺 The five checks

Every machine gets the same five timestamped checks before anything is changed.

| Check | Why it matters |
|---|---|
| 🧱 **Component store** | A damaged component store blocks updates from installing |
| 🔄 **Pending reboot** | An unfinished restart holds the next update back |
| 🧰 **Servicing stack** | An outdated servicing stack can't apply newer updates |
| 🔢 **Update error code** | The error Windows Update reported points to the cause |
| 💾 **System volume** | Too little free space on the system drive stops the install |

## 🛡️ Guardrails

<img src="assets/guardrails.svg" width="100%" alt="Six things FastPatch will never do: restart your machines, change Windows Update settings, delete Windows repair files, touch antivirus or security tools, loop without a limit, say success without proof.">

## 🚦 Every machine gets an answer

<img src="assets/outcomes.svg" width="100%" alt="Six outcomes: fixed itself, try again later, waiting for a restart, needs a decision, needs an engineer, rolled back.">

When FastPatch can't finish a machine, it never fails silently. It hands the machine back with one of six labels, so nobody has to work out what happened.

## ⚖️ Before and after

| Step | 😩 Before | ⚡ With FastPatch |
|---|---|---|
| Find failures | Export to a sheet, filter and clean by hand | Read straight from Kaseya patch status |
| Choose machines | Judged one by one from the sheet | Eligibility checked by rules on the machine |
| Diagnose | Log in and run the checks manually | Five checks on the agent, each timestamped |
| Name the cause | Depends on who picks it up | One reason from a shared vocabulary |
| Fix | Ad hoc, then retry | The approved path for that reason |
| Prove it landed | "The job ran" | The update is present after the restart |
| Report | Free-text ticket notes | A ticket-ready line: cause plus action |

## 📈 Results in production

| 🖥️ Machines patched | ✅ Success rate | 📏 Fleet size |
|:-:|:-:|:-:|
| **600+** across client fleets | **99%** patched cleanly, the rest handed back with a named cause | **10 → 100+** machines on the same flow |

## 🗺️ Roadmap

| | Item | Status |
|:-:|---|---|
| 🪟 | Windows patch remediation through Kaseya VSA | ✅ Live in production |
| 🔁 | Auto-rollback for Windows | 🆕 New, in beta |
| 🍎 | macOS patching | 🆕 New, in beta |
| 🔂 | Reboot proof | 📝 Planned |
| 📊 | Central result collection | 📝 Planned |
| 🩺 | Health checks | 📝 Planned |

## ❓ FAQ

<details>
<summary><b>Will FastPatch restart our machines?</b></summary>
<br>
No. Your maintenance window restarts machines, on your schedule. FastPatch only checks afterwards that the update really installed.
</details>

<details>
<summary><b>Do we have to install anything new?</b></summary>
<br>
No new app goes on your machines. FastPatch runs inside the Kaseya VSA you already have, as a signed procedure scheduled per machine group.
</details>

<details>
<summary><b>Will it change our Windows Update settings or policy?</b></summary>
<br>
No. It works with whoever manages updates today and never rewrites update policy.
</details>

<details>
<summary><b>What happens when it can't fix a machine?</b></summary>
<br>
The machine comes back with one of six labels: fixed itself, try again later, waiting for a restart, needs a decision, needs an engineer, or rolled back. Your NOC works those exceptions only.
</details>

<details>
<summary><b>Who approves the fixes?</b></summary>
<br>
You do. FastPatch applies only the approved path for each cause, inside your approval policy, and rolls out one machine group at a time.
</details>

<details>
<summary><b>How large a fleet can it handle?</b></summary>
<br>
It runs the same flow on 10 machines or 100+, and has patched 600+ machines in production so far.
</details>

<details>
<summary><b>What if a patch breaks a machine?</b></summary>
<br>
Auto-rollback compares the machine with its pre-patch baseline after your restart window. If a service that ran before is down, a required service is down, or Windows crashed, it removes only the new update, with no restart forced, and confirms it's gone after the next restart.
</details>

<details>
<summary><b>Does it support Macs?</b></summary>
<br>
Yes, in beta. FastPatch patches Macs through Apple's softwareupdate with the same guardrails. On Apple silicon, updates that need a restart are downloaded and wait for a user or MDM to authorise them, because Apple requires that.
</details>

<details>
<summary><b>Can it roll back a Mac update?</b></summary>
<br>
No. Apple doesn't support removing installed macOS updates, so auto-rollback is Windows only.
</details>

<details>
<summary><b>How was it built?</b></summary>
<br>
FastPatch was designed and built with Claude as a design partner. People review and approve every production release.
</details>

More detail lives in [`docs/`](docs).

## 🚀 Get FastPatch

FastPatch is closed source and offered to MSPs directly. The quickest way to see it is a live demo on a Kaseya console, followed by a pilot on one of your machine groups.

<div align="center">

<a href="mailto:rehank9540@gmail.com?subject=FastPatch%20demo"><img src="https://img.shields.io/badge/⚡_Book_a_demo-3FD07A?style=for-the-badge&labelColor=0B1730" alt="Book a FastPatch demo"></a>
<a href="mailto:rehank9540@gmail.com?subject=FastPatch%20pilot%20for%20our%20MSP"><img src="https://img.shields.io/badge/🧪_Pilot_it_on_your_fleet-38C8F0?style=for-the-badge&labelColor=0B1730" alt="Pilot FastPatch on your fleet"></a>

</div>

## 📁 What's in this repo

```
fastpatch/
├── README.md            you are here
├── docs/
│   ├── how-it-works.md  the run loop and the five checks in detail
│   ├── guardrails.md    what FastPatch will never do, and the six outcomes
│   ├── auto-rollback.md how a bad patch is detected, removed and proven gone
│   ├── macos.md         Mac patching (beta): what it installs and what it waits on
│   └── faq.md           answers for MSP owners, NOC leads and security teams
├── assets/              README graphics (animated SVG)
├── tools/
│   └── build_assets.py  regenerates every graphic in assets/
├── CHANGELOG.md
├── SECURITY.md
└── LICENSE.md
```

This repository is the public home of FastPatch: documentation and product information. The FastPatch engine itself is not distributed here.

---

<div align="center">
<sub>Built by <a href="https://github.com/rehan-123">Rehan Khan</a> · The run log in the header graphic is illustrative, with made-up host names · Kaseya and Kaseya VSA are trademarks of Kaseya Limited; FastPatch is not affiliated with Kaseya.</sub>
</div>
