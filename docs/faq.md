# FAQ

## For MSP owners

**What does FastPatch change for my team?**
Engineers stop exporting failures to a spreadsheet and diagnosing machines one by one. They read a short list of exceptions, each with its cause already named.

**Is it proven?**
It is live in production and has patched 600+ machines across client fleets at a 99% success rate. The remaining machines were handed back with a named cause.

**How do we start?**
With a demo on a Kaseya console, then a pilot on one machine group. Email [rehank9540@gmail.com](mailto:rehank9540@gmail.com?subject=FastPatch%20demo).

## For NOC leads

**Does it replace Kaseya patch management?**
No. It works alongside it: Kaseya still schedules, runs and logs. FastPatch adds diagnosis, the approved fix and proof that the update landed.

**How large a fleet can it handle?**
The same flow runs on 10 machines or 100+.

**What do we get back from each run?**
One line per machine with status, cause and action, plus one of five outcome labels. See [guardrails](guardrails.md#the-five-outcomes).

## For security teams

**Does it restart machines or change update policy?**
No to both. See the full list of [guardrails](guardrails.md).

**Does it install new software on endpoints?**
No. It runs through the Kaseya agent that is already there, as a signed procedure.

**Does it touch antivirus or other security tools?**
No.

**Who approves changes?**
Every production release is approved by a person, and fixes stay inside the client's approval policy.

## Platform

**Which operating systems are supported?**
Windows today. macOS support is the next build.
