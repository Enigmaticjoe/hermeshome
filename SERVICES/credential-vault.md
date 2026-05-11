# Chimera Credential Vault

> **MCP Server:** `credential-vault` on Node C (:8011)
> **Encryption:** AES-256-GCM (PBKDF2 key derivation, 600K iterations)
> **Storage:** SQLite at `~/.credential-vault/vault.enc`
> **Credentials:** 34 across 10 groups (as of 2026-05-10)

## Access

The vault is available as an MCP server. Connect any MCP-compatible client:

```
http://192.168.1.6:8011/sse
```

**Unlock key:** `CREDENTIAL_VAULT_KEY` environment variable
**Systemd:** `mcp-credential-vault.service` (auto-restarts)

## Tools

| Tool | Description | Returns values? |
|------|-------------|----------------|
| `get_credential(name)` | Retrieve a specific credential | ✅ Full decrypted value |
| `list_credentials()` | List all credential names | ❌ Metadata only |
| `set_credential(name, value, group, notes)` | Add or update | N/A |
| `delete_credential(name)` | Remove a credential | N/A |
| `search_credentials(query)` | Search by name, group, or notes | ❌ Metadata only |
| `get_credential_group(group)` | Get all credentials in a group | ❌ Metadata only |
| `vault_stats()` | Total count and group count | N/A |
| `set_bulk_credentials(json_array)` | Bulk import from JSON | N/A |

## Credential Groups

| Group | Count | Examples |
|-------|-------|---------|
| ssh | 5 | All 5 node SSH passwords |
| web | 7 | Media Portal, Portainer, Forgejo, HA, Hermes |
| api | 7 | DeepSeek, LiteLLM, Plex, Prowlarr, Authelia, HA, MCP |
| cloudflare | 4 | Account ID, API token, Global key, Origin CA |
| tailscale | 1 | Auth key |
| proxmox | 2 | Node D, Node E |
| unraid | 1 | Web password |
| database | 3 | Forgejo, Langfuse passwords |
| mcp | 2 | HA token + URL |
| storage | 2 | SMB guest, NFS mount |

## Adding New Credentials

```bash
# Via MCP tool
set_credential(name="my_new_key", value="sk-xxx", group="api", notes="Description")

# Or update the seed script and re-run
# File: ~/git/shite/mcp/servers/credential-vault/seed_vault.py
export CREDENTIAL_VAULT_KEY=chimera-vault-master-2026
cd ~/git/shite/mcp/servers/credential-vault
~/git/shite/.venv/bin/python seed_vault.py
```
