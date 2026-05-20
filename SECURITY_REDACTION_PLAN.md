# SECURITY_REDACTION_PLAN.md — HermesHome Credential Cleanup

> Generated: 2026-05-20
> Status: DRAFT — requires ARMED approval before execution
> Repository: Enigmaticjoe/hermeshome

## Summary

**CRITICAL:** This public GitHub repo contains live credentials — SSH passwords, API keys, Cloudflare Global Key, and service passwords in plaintext. The `.gitignore` was added late; check `git log --all --diff-filter=A -- .gitignore` to see if secrets were committed before it existed.

## Files Containing Suspected Secrets

### 1. CREDENTIALS/reference.md — LIVE PASSWORDS
| Line | Secret Type | Value Leaked | Risk |
|------|-------------|-------------|------|
| 7 | SSH password | `1212` (Node A jb) | HIGH — direct root access |
| 8 | SSH password | `12121212` (Node B root) | HIGH |
| 10 | SSH password | `12121212` (Node D root) | HIGH |
| 11 | SSH password | `12121212` (Node E root) | HIGH |
| 16 | Web login | `josh / 12121212` Media Portal | HIGH |
| 17 | Web login | `admin / 121212121212` Portainer | HIGH |
| 18 | Web login | `jbauer / 12121212` Forgejo | HIGH |
| 19 | Web login | `admin / 12121212` Pi-hole | HIGH |
| 20 | Web login | `jb / 12alora34` Home Assistant | HIGH |
| 21 | Web login | `admin / 12alora34` Hermes WebUI | HIGH |
| 27 | API key | `sk-master-key` LiteLLM | HIGH |
| 28 | API key | `AQzj8-4b56cZddtn9Q6q` Plex Token | MEDIUM |
| 29 | API key | `fc508a712b5b4d4e96884faf15e886c3` Prowlarr | MEDIUM |
| 30 | Secret | `65fca9db4f0243a95453927839e20239` Authelia Session | HIGH |

**Fix:** Replace every value with `${ENV_VAR_NAME}` or `{{PLACEHOLDER}}`. Move actual values to `secrets/chimera-secrets.yaml` (already `.gitignore`-d).

### 2. CONFIGS/hermes/config.yaml — LIVE API KEYS
| Line | Secret Type | Value Leaked | Risk |
|------|-------------|-------------|------|
| 5 | DeepSeek API key | `sk-c282255adfea44cdb9b3336f99630dc9` | **CRITICAL** — $0.50-$2/week, usable until rotated |
| 16 | vLLM API key | `eme0wno4htu3` | LOW — local-only |
| 100 | sudo password | `1212` | HIGH — full system access |

**Fix:** Replace `sk-c2822...` with `${DEEPSEEK_API_KEY}`. Replace `1212` with `${SUDO_PASSWORD}`. These should be env vars passed to Hermes, not hardcoded.

### 3. SERVICES/litellm/litellm-config.yaml — LIVE MASTER KEY
| Line | Secret Type | Value Leaked | Risk |
|------|-------------|-------------|------|
| 8, 93 | LiteLLM master key | `sk-master-key` | HIGH — full API gateway access |

**Fix:** Replace with `LITELLM_MASTER_KEY` env var reference per LiteLLM docs.

### 4. SERVICES/pihole/docker-compose.yml — LIVE PASSWORD
| Line | Secret Type | Value Leaked | Risk |
|------|-------------|-------------|------|
| 11 | Web password | `12121212` | HIGH |

**Fix:** Replace with `${PIHOLE_WEBPASSWORD}` env var.

### 5. CHIMERA_REPORT.md — COMPREHENSIVE LEAK
| Line(s) | Secret Type | Value Leaked | Risk |
|---------|-------------|-------------|------|
| 247 | **Cloudflare Global API Key** | `18f0b0c4c443d0c2b562d7a2ffd4667f5d312` | **CRITICAL** — Full Cloudflare account access |
| 164, 181, 193, 218, 220 | SSH passwords | `12121212` × multiple | HIGH |
| 272-273, 281-282 | Proxmox credentials | `root@pam / 12121212` | HIGH |
| 291 | LiteLLM key | `sk-master-key` | HIGH |
| 301 | Portainer | `admin / 121212121212` | HIGH |
| 429, 803, 925 | API keys | `sk-master-key` | HIGH |
| 791-795, 809, 852, 874 | Security audit section | Documents all passwords in plaintext | HIGH |

**Fix:** Regenerate this entire file without secrets. This is a 35KB dump meant for ChatGPT — it should NOT contain live credentials. Strip all passwords, keys, and tokens from the output version.

### 6. DNS/pihole.md
| Line | Secret Type | Value Leaked | Risk |
|------|-------------|-------------|------|
| 7 | Password | `12121212` | HIGH |

**Fix:** Replace with `${PIHOLE_WEBPASSWORD}`.

## Replacement Strategy

For each file, the pattern is:
```
old: password: "12121212"
new: password: "${SERVICE_PASSWORD}"     # set via env file
```

### Env File Structure (to be created)
Create `CONFIGS/env/chimera.env.example` with ALL variables in placeholder form:

```bash
# ── API Keys ──
DEEPSEEK_API_KEY=sk-your-deepseek-key
LITELLM_MASTER_KEY=sk-your-litellm-key
CLOUDFLARE_API_KEY=your-cloudflare-global-key
CLOUDFLARE_EMAIL=your@email.com
TAILSCALE_AUTH_KEY=tskey-auth-xxxxx

# ── Passwords ──
SSH_PASSWORD_NODE_A=your-password
SSH_PASSWORD_NODE_B=your-password
SSH_PASSWORD_NODE_D=your-password
SSH_PASSWORD_NODE_E=your-password
SUDO_PASSWORD=your-sudo-password

# ── Service Passwords ──
PORTAINER_PASSWORD=your-portainer-password
PIHOLE_WEBPASSWORD=your-pihole-password
AUTHELIA_SESSION_SECRET=your-session-secret
HERMES_WEBUI_PASSWORD=your-hermes-password
HA_PASSWORD=your-ha-password
FORGEJO_PASSWORD=your-forgejo-password

# ── Tokens ──
PLEX_TOKEN=your-plex-token
PROWLARR_API_KEY=your-prowlarr-key
HOME_ASSISTANT_TOKEN=your-ha-long-lived-token
TELEGRAM_BOT_TOKEN=your-bot-token

# ── Model Config ──
HERMES_MODEL=hermes-auto
LITELLM_BASE_URL=http://192.168.1.222:4000/v1
```

### .gitignore Update
The current `.gitignore` already covers `.env*`, `secrets/`, and `credentials/`. Add:
```
# Config files with placeholders are fine, but no live secrets
# The following files have been redacted — content is safe to commit

# Add CHIMERA_REPORT.md to the redaction verification list
```

## Rotation Checklist

After the redaction is committed, rotate ALL of the following:

| Service | Rotation Method | Priority |
|---------|----------------|----------|
| Cloudflare Global API Key | Generate new key in Cloudflare Dashboard | **IMMEDIATE** |
| DeepSeek API Key | Regenerate at platform.deepseek.com | **IMMEDIATE** |
| Tailscale Auth Key | Regenerate at Tailscale admin console | **HIGH** |
| LiteLLM master_key | Change in docker-compose env, restart | **HIGH** |
| Telegram Bot Token | Revoke via @BotFather, generate new | **HIGH** |
| Gmail App Password | Revoke at accounts.google.com (App Passwords) | **MEDIUM** |
| Home Assistant Token | Generate new long-lived token in HA profile | **MEDIUM** |
| Plex Token | Revoke devices, re-auth | **LOW** |
| Prowlarr API Key | Regenerate in Prowlarr settings | **LOW** |
| Authelia Session Secret | Change in config, all sessions invalidated | **MEDIUM** |

## ARMED Approval Required

The following changes are DESTRUCTIVE and require you to type:
```
ARMED hermeshome secret-redaction
```

1. **Rewriting CHIMERA_REPORT.md** — 35KB file used by ChatGPT, must preserve utility while stripping secrets
2. **Replacing live values in config.yaml** — Hermes will need the env vars set before restart
3. **Rewriting CREDENTIALS/reference.md** — Replace all live values with placeholders

## Non-Destructive Changes (safe to do now)
- Create `CONFIGS/env/chimera.env.example` (new file)
- Update `.gitignore` (additions only)
- Update `DNS/pihole.md` password reference

## Verifying the Fix

After redaction:
```bash
cd ~/git/hermeshome
# Check for any remaining secrets
rg -n -e '(sk-[a-zA-Z0-9]{20,})' -e '(12121212|1212[^2])' -e '18f0b0c4' --no-ignore-vcs | grep -v '.git/'
# Should produce NO output
```
