# Hermes Desktop Update Risk — Windows

Observed profile: Windows desktop app, multiple Hermes profiles under `AppData\Local\hermes\profiles\{default,prime,assist}`, separate root `config.yaml` plus per-profile configs, recent model/provider reconfiguration.

## High-Risk Changelog Signals
- `state.db` / migration / session-metadata changes.
- Revert-of-feature PRs touching approval/tool-call flows.
- Config redaction, streaming body-read, env-lookup changes.
- Gateway-parent metadata consolidation.

## Safe Default
Postpone. Require Mod A risk translation + explicit R0 before update.

## Backup Surface
- root: `config.yaml`, `SOUL.md`, `CONSTINTA.md`
- per-profile: `config.yaml`, `SOUL.md`, directory tree timestamp
- logs: `AppData\Local\hermes\logs`

## Decision Template
1. Current state → working or degraded?
2. Update fixes exactly the user's pain points?
3. Backup present + restore path known?
4. User explicit R0 for update?

Reference session: 2026-07-06 update dialog + user history of post-update breakage after Antigravity-tuned model list/profile setup.
