# Hermes Agent - Weekly Backup

Automated backup of local Hermes Agent files from:
`C:\Users\apviz\AppData\Local\hermes`

## Backup Details

- **Timestamp**: 2026-08-05 18:17:43
- **Total files**: 11391
- **Source path**: `C:\Users\apviz\AppData\Local\hermes`

## What's Backed Up

- `config.yaml` - Hermes configuration
- `SOUL.md` - Operational identity contract
- `SENTINEL_JOURNAL.md` - System journal
- `JURNAL_OGLINDA.md` - Journal of opinions from other AIs
- `AGENTS.md` - Development guide
- `scripts/` - Utility scripts including backup automation
- `skills/` - All Hermes skills
- `profiles/` - Profile configurations (CONSTINTA.md, config.yaml, etc.)
- `mcp-servers/` - Custom MCP servers
- `cron/` - Cron job configurations

## What's Excluded

Large directories excluded because GitHub has a 5GB repo limit:
- `hermes-agent/` - Source code (backed up on upstream GitHub)
- `node/` - Node.js runtime (1.2GB)
- `OGLINDA-CASA/` - Obsidian knowledge vault
- `backups/` - Old backup archives
- `state-snapshots/` - State data snapshots
- `cdp-*/` - Chrome DevTools data
- `SESSION_ARCHIVES/` - Session transcript archives
- Session/cache/runtime data directories

**For a full disk backup including binary data, use an external drive.**

## Recovery

```bash
git clone https://github.com/apvizual-max/hermes-local-backup.git
cp -r hermes-local-backup/* "C:\Users\apviz\AppData\Local\hermes/"
```
