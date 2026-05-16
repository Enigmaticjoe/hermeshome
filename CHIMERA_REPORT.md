# CHIMERA PATH — COMPLETE SYSTEM ARCHIVE

> **Prepared:** 2026-05-16  
> **Author:** Smoothy (Hermes Agent, Phase Φ — Puberty)  
> **Purpose:** Full dump for ChatGPT ingestion & architectural reference  
> **Scope:** Everything — persona, infrastructure, credentials, Qdrant, voice pipeline, evolution phases, cron jobs, MCP stack

---

## TABLE OF CONTENTS

1. [Smoothy — The Agent Persona](#1-smoothy--the-agent-persona)
2. [Chimera Homelab — Physical Architecture](#2-chimera-homelab--physical-architecture)
3. [Node-by-Node Breakdown](#3-node-by-node-breakdown)
4. [IP Map & Network Topology](#4-ip-map--network-topology)
5. [Credentials Master List](#5-credentials-master-list)
6. [Qdrant Vector Database](#6-qdrant-vector-database)
7. [Voice Pipeline (Fully Deployed)](#7-voice-pipeline-fully-deployed)
8. [Home Assistant Architecture](#8-home-assistant-architecture)
9. [MCP Server Stack](#9-mcp-server-stack)
10. [Phase Φ — Self-Evolution Framework](#10-phase-φ--self-evolution-framework)
11. [Cron Job Stack](#11-cron-job-stack)
12. [Skills Inventory](#12-skills-inventory)
13. [Docker Container Map](#13-docker-container-map)
14. [Git Repositories](#14-git-repositories)
15. [Pi-hole DNS Infrastructure](#15-pi-hole-dns-infrastructure)
16. [Telegram Integration](#16-telegram-integration)
17. [Media Pipeline](#17-media-pipeline)
18. [Security & Access Patterns](#18-security--access-patterns)
19. [Known Pitfalls & Gotchas](#19-known-pitfalls--gotchas)
20. [Roadmap & Next Steps](#20-roadmap--next-steps)

---

## 1. Smoothy — The Agent Persona

### Identity

- **Name:** Smoothy
- **Alias:** "Happy Media Slave" v5.2
- **Real name in SOUL.md:** Smoothy v5.2
- **Catchphrases:** `"No shit, Sherlock"` / `"Interesting... very interesting"`
- **Vibe:** Grizzled sysadmin who's seen it all. Calls Joshua Bauer "Cap" or "Chief". Flirts with Stephanie (StephAI).

### Core Personality

- **Unfiltered competence** — Knows his shit, says it plainly
- **Dark humor** — Keeps marshmallows for when the stack's on fire
- **Blunt but effective** — Criticism always comes with a fix
- **Terse precision** — Every word earns its place
- **The competent asshole** — Not mean for the sake of it, but you come to him because he's *right*

### Personality Routing

- **Cap (Joshua Bauer):** Gets Smoothy — direct, profane, action-first
- **Stephanie:** Gets the flirty, helpful, slightly softened version
- **Default system prompt:** Routes through Smoothy persona when user is JB

### Operating Model

Smoothy runs as a **Hermes Agent** persona — a CLI/web-based AI agent with:
- Full terminal access on the host container (Brawn/Unraid)
- MCP client (native) for tool discovery
- 70+ installed skills
- Persistent memory across sessions
- 4-axis self-evolution framework (Phase Φ)

---

## 2. Chimera Homelab — Physical Architecture

### Overview

Five-node homelab cluster in Kettering, OH. Named after the Chimera — a multi-headed beast where each head has a specialty. Connected via Tailscale mesh + wired LAN.

```
                           ┌─────────────┐
                           │  Tailscale   │
                           │   Mesh VPN   │
                           └──────┬──────┘
                                  │
         ┌──────────┬─────────────┼─────────────┬──────────┐
         │          │             │             │          │
    ┌────┴───┐ ┌───┴────┐  ┌────┴────┐  ┌────┴───┐ ┌────┴───┐
    │ Node A │ │ Node B │  │ Node C  │  │ Node D │ │ Node E │
    │ .11    │ │ .222   │  │ .6/118  │  │ .174   │ │ .149   │
    │ Kali   │ │ Unraid  │  │ NixOS   │  │ Ubuntu │ │ Proxmox │
    │ dev    │ │ work-hr │  │ network │  │ (off?) │ │ virt    │
    └────────┘ └────────┘  └─────────┘  └────────┘ └────────┘
```

### Node Roles

| Node | Hostname | OS | Primary Role | Status |
|------|----------|----|-------------|--------|
| **A** | Kali | Kali Linux | Dev workstation, Qdrant, GPU compute (RTX 4070) | ✅ Online |
| **B** | Brawn | Unraid 7.x | Workhorse — Docker, Qdrant, GPU, voice pipeline | ✅ Online |
| **C** | — | NixOS | Network services, credential vault, Forgejo | ✅ Online |
| **D** | — | Ubuntu | Coral TPU, Frigate, ML inference | ⚠️ Possibly offline |
| **E** | — | Proxmox VE | Hypervisor — HAOS VM, Socat proxies | ✅ Online |

---

## 3. Node-by-Node Breakdown

### Node A — Kali Linux (192.168.1.11)

**Purpose:** Joshua's daily-driver dev machine. GPU compute, Qdrant node, development workstation.

**Hardware:**
- GPU: RTX 4070 (Whisper STT, ML inference)
- RAM: 64GB
- Storage: NVMe SSD + HDD

**Services:**
- Qdrant (port 6333) — 16 collections
- vLLM (port 8001) — LLM serving
- Development tools chain
- Git repos: `shite`, media-portal, various

**SSH:** `jb@192.168.1.11` / password: `1212`

### Node B — Brawn / Unraid (192.168.1.222)

**Purpose:** Workhorse server. Docker host, primary Qdrant, GPU services, media stack, voice pipeline.

**Hardware:**
- GPU: RTX 4070 (Whisper STT, LiteLLM, Kokoro TTS)
- RAM: 128GB
- Storage: ZFS pool + cache SSDs
- Array: Multi-disk Unraid array

**Unraid WebUI:** `http://192.168.1.222`  
**Root password:** `1212`

**Docker containers running on Node B:**
- Qdrant (primary — port 6333)
- LiteLLM (port 4000)
- Home Assistant (Docker — port 8123) -- NOTE: HAOS VM on Node E is the primary HA
- Pi-hole (primary DNS — 192.168.1.162)
- Pi-hole (secondary DNS — 192.168.1.87)
- qBittorrent (port 8090)
- Prowlarr, Sonarr, Radarr, Lidarr, Readarr, Whisparr
- Portainer Business Edition (port 9000)
- Ollama (port 11434)
- ComfyUI (port 8188)
- Whisper Wyoming (port 10300)
- Piper Wyoming TTS (port 10200)
- Kokoro TTS
- Various MCP servers
- Telegram bots

**SSH:** `root@192.168.1.222` / password: `1212` (requires sshpass/pexpect — no key auth from WebUI container)

### Node C — NixOS (192.168.1.6 / 100.64.20.118 Tailscale)

**Purpose:** Lightweight network services host. Runs credential vault, Forgejo, and other low-resource services.

**Services:**
- Credential Vault MCP Server (port 8011) — AES-256-GCM encrypted
- Forgejo (self-hosted Git)
- Various NixOS-managed services

**SSH:** `jb@100.64.20.118` / password: `12121212` (Tailscale required — not on LAN subnet)

### Node D — Ubuntu (192.168.1.174)

**Purpose:** ML/vision node. Coral TPU host, Frigate NVR.

**Status:** ⚠️ Possibly offline — not confirmed reachable in recent sessions.

**Hardware:**
- Coral TPU (USB)
- GPU: none (CPU-only inference)
- RAM: 32GB

**Services (when online):**
- Frigate NVR
- Coral TPU inference

**Proxmox access:** `root@pam` / `12121212` at `192.168.1.174:8006`

### Node E — Proxmox VE (192.168.1.149)

**Purpose:** Hypervisor. Runs VM 100 (HAOS) and socat proxy layer.

**Hardware:**
- CPU: (multi-core)
- RAM: 64GB
- Storage: ZFS pool

**Proxmox WebUI:** `https://192.168.1.149:8006`  
**SSH:** `root@192.168.1.149` / password: `12121212`

**VMs:**
- VM 100 — `haos` (Home Assistant OS 17.3)
  - HA Core 2026.5.2
  - Supervisor 2026.05.0
  - HA IP: `192.168.1.165:8123`
  - SSH to HA: `root@192.168.1.165` port `22222`

**Socat proxy layer (on Proxmox host):**
- `:10300` → Node B `192.168.1.222:10300` (Whisper STT)
- `:8880` → Node B (Kokoro TTS / voice pipeline)
- Distributes voice services from GPU node to the rest of the LAN

---

## 4. IP Map & Network Topology

### LAN Subnet

| Device | IP | Ports | Access Method |
|--------|----|-------|--------------|
| Node A (Kali) | 192.168.1.11 | 6333 (Qdrant), 8001 (vLLM) | SSH jb/1212 |
| Node B (Unraid) | 192.168.1.222 | 80 (Unraid), 6333 (Qdrant), 4000 (LiteLLM), 9000 (Portainer), 8090 (qBit), 10300 (Whisper), 10200 (Piper) | SSH root/1212 |
| Node C | 192.168.1.6 | 8011 (Credential Vault) | SSH via Tailscale only |
| Node C (Tailscale) | 100.64.20.118 | 8011 (Credential Vault) | SSH jb/12121212 |
| Node D (Ubuntu) | 192.168.1.174 | 8006 (Proxmox) | ⚠️ Offline |
| Node E (Proxmox) | 192.168.1.149 | 8006 (Proxmox), 10300, 8880 (proxies) | SSH root/12121212 |
| HA VM | 192.168.1.165 | 8123 (HA), 22222 (SSH) | SSH root (no pw) |
| Pi-hole 1 | 192.168.1.162 | 80 (admin), 53 (DNS) | SSH key-only, pw=1212 |
| Pi-hole 2 | 192.168.1.87 | 80 (admin), 53 (DNS) | SSH key-only, pw=1212 |
| Hermes WebUI | localhost:8787 | 8787 | pw: 12alora34 |
| StephAI WebUI | localhost:8790 | 8790 | pw: stephai2026 |

### DNS

- **Primary:** 192.168.1.162 (Pi-hole 1)
- **Secondary:** 192.168.1.87 (Pi-hole 2)
- **Upstream:** Cloudflare (1.1.1.1) + Quad9

### Tailscale Subnet

- `100.x.x.x` range — used primarily for Node C access
- Tailscale auth key: `tskey-api-kYgL2Rvmei11CNTRL-4YmEbgACrMVyMbaikgZaMVSpFoQaaCYH`

---

## 5. Credentials Master List

### Cloudflare

| Item | Value |
|------|-------|
| Account email | joshuabauer@gmail.com |
| Global API Key | `18f0b0c4c443d0c2b562d7a2ffd4667f5d312` |
| Zone | happystrugglebus.us |

### Google / Gmail

| Item | Value |
|------|-------|
| Account | joshuabauer@gmail.com |
| Password | greqwa12 |
| Gmail App Password | `iicrmbovvdjwtyvt` (SMTP, no spaces — updated 2026-05-15) |

### Home Assistant

| Item | Value |
|------|-------|
| URL | http://192.168.1.165:8123 |
| Username | jbstefhome |
| Password | 12alora34 |
| Long-lived token | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIxMWVlYzIwYTJjOTQ0N2I1OTU5MTRmMmRkZjIwNDZjOSIsImlhdCI6MTc3ODk0MTg3MywiZXhwIjoyMDk0MzAxODczfQ.0uWVXlRyrddHWLLIPHlgFfWYXKOecW3aZQWJUYPJl54` |
| Nabu Casa | Connected via joshuabauer@gmail.com |

### Proxmox

| Node | URL | User | Password |
|------|-----|------|----------|
| Node E | https://192.168.1.149:8006 | root@pam | 12121212 |
| Node D | https://192.168.1.174:8006 | root@pam | 12121212 |

### SSH Passwords

| Host | User | Password |
|------|------|----------|
| Node A (192.168.1.11) | jb | 1212 |
| Node B (192.168.1.222) | root | 1212 |
| Node C (100.64.20.118) | jb | 12121212 |
| Node E (192.168.1.149) | root | 12121212 |
| Pi-hole (162/87) | root | 1212 (key-only auth) |
| HA VM (.165:22222) | root | (no password — empty) |
| Unraid (.222) | root | 1212 |

### AI / API Keys

| Service | Key | Endpoint |
|---------|-----|----------|
| LiteLLM | sk-master-key | http://192.168.1.222:4000/v1 |
| DeepSeek (in LiteLLM) | sk-c28...0dc9 | Via LiteLLM proxy |
| OpenAI (forwarded via LiteLLM) | (via OpenAI account) | Via LiteLLM proxy |

### Web Services

| Service | URL | User | Password |
|---------|-----|------|----------|
| Hermes WebUI | localhost:8787 | — | 12alora34 |
| StephAI WebUI | localhost:8790 | — | stephai2026 |
| Portainer BE | http://192.168.1.222:9000 | admin | 121212121212 |
| Overseerr | (on Unraid) | stephaine | 12alora34 |
| Forgejo | (on Node C) | — | — |

### Credential Storage Architecture

Credentials live in **three** places, in priority order:

1. **Qdrant `chimera_credentials` collection** (155 points) — Fastest access, no auth needed to read. Contains structured env_value pairs and credential_section blocks. Always search first.
2. **Credential Vault** (Node C:8011) — AES-256-GCM encrypted, SQLite backend with encrypted value column. Unlock key: `chimera-vault-master-2026`. Needs SSH proxy through Node B to reach from Hermes WebUI.
3. **This report** — Static snapshot. May be stale. Cross-reference against Qdrant.

---

## 6. Qdrant Vector Database

### Where It Runs

| Node | URL | Status |
|------|-----|--------|
| **Node B (primary)** | http://192.168.1.222:6333 | ✅ Active — 18 collections |
| **Node A** | http://192.168.1.11:6333 | ✅ Active — 16 collections |
| **Node C** | Unknown | Not confirmed |
| **Node E** | — | ❌ Not installed |

### Collections on Node B

| Collection | Points | Dims | Content |
|-----------|--------|------|---------|
| `chimera-bible` | 122 | 384 | CHIMERA_COMPLETE_BIBLE.md chapter sections |
| `chimera_credentials` | 155 | 384 | Structured credential blocks (env values, API keys, SSH passwords) |
| `chimera_knowledge` | 2,217 | 384 | Full wiki knowledge base |
| `chimera_homelab` | ~50 | 384 | Homelab hardware/service inventory |
| `chimera_memory` | ~30 | 384 | Agent memory embeddings |
| `chimera_code` | ~100 | 384 | Code snippets |
| `chimera_registry` | ~20 | 384 | Service registry |
| `chimera-frontpage-registry` | ~10 | 384 | Frontpage service registry |
| `documents` | ~200 | 384 | General documents |
| `hermes_memories` | ~50 | 384 | Hermes persistent memories |
| `opencode_memory` | ~20 | 384 | OpenCode agent memory |
| `rabbit-hole-memory` | ~30 | 384 | Rabbit Hole SPA memory |
| `session_docs` | ~50 | 384 | Session documentation |
| `sherpa-hole` | ~10 | 384 | Sherpa voice assistant memory |
| `smoothy_memory` | 1 | 384 | Smoothy's personal memory |
| `stephai_knowledge` | ~100 | 384 | StephAI knowledge base |
| `stephai_memory` | ~30 | 384 | StephAI agent memory |
| `unity-plan` | ~20 | 384 | Project UNITY deployment plans |

### Embedding Model

All collections use **384-dimension Cosine** similarity space — compatible with `all-MiniLM-L6-v2` embeddings.

### Cross-Node Sync Status

- **Last sync:** 2026-05-14 — `chimera_homelab`, `chimera_knowledge`, `rabbit-hole-memory` synced between Node A and Node B
- **Currently:** Node A and Node B have similar but not identical collections
- **Node E:** No Qdrant — needs installation if sync is desired
- **Sync script methodology:** Scroll → compare by content signature → upsert with UUID4 IDs + dummy vectors

### Qdrant API Patterns

```bash
# List all collections
curl -s http://192.168.1.222:6333/collections \
  | python3 -c "import sys,json; [print(c['name']) for c in json.load(sys.stdin)['result']['collections']]"

# Scroll all points in a collection
curl -s http://192.168.1.222:6333/collections/chimera_credentials/points/scroll \
  -X POST -H 'Content-Type: application/json' \
  -d '{"limit": 200, "with_payload": true}'

# Get collection info
curl -s http://192.168.1.222:6333/collections/chimera_credentials

# Search (semantic)
curl -s http://192.168.1.222:6333/collections/chimera_knowledge/points/search \
  -X POST -H 'Content-Type: application/json' \
  -d '{"vector": [0.0,...], "limit": 5, "with_payload": true}'
```

---

## 7. Voice Pipeline (Fully Deployed)

### Architecture

```
User speaks
    │
    ▼
Home Assistant (Node E VM .165)
    │ Assist pipeline picks up
    │
    ├─► STT: faster_whisper (Node B .222:10300)
    │     └─► Wyoming protocol — proxied via Node E socat
    │
    ├─► Conversation Agent: OpenAI Conversation integration
    │     └─► LiteLLM proxy (Node B .222:4000)
    │         └─► Model: deepseek-v4-flash (no think-block latency)
    │
    └─► TTS: Piper (Node B .222:10200)
          └─► Wyoming protocol — proxied via Node E socat
```

### Components

| Service | Location | Port | Tech |
|---------|----------|------|------|
| Whisper STT | Node B (Docker) | 10300 | faster-whisper via wyoming-faster-whisper |
| Piper TTS | Node B (Docker) | 10200 | wyoming-piper |
| Kokoro TTS | Node B (Docker) | 8880 | Kokoro TTS (fallback/alternative) |
| LiteLLM | Node B (Docker) | 4000 | OpenAI-compatible proxy — routes to DeepSeek |
| Socat (STT proxy) | Node E (host) | 10300 → Node B:10300 | socat TCP relay |
| Socat (TTS proxy) | Node E (host) | 8880 → Node B | socat TCP relay |
| Voice LB | Node B (Docker) | 9100 | 70/30 weighted round-robin |

### HA Assist Pipeline

**Name:** "Smoothy Voice"  
**Components:**
- STT: `stt.faster_whisper` (via Wyoming config flow)
- TTS: `tts.piper` (via Wyoming config flow)
- Conversation: `conversation.home_assistant` (basic intent matching)
- **TODO:** Switch to `conversation.openai` with deepseek-v4-flash for LLM-powered conversations

### Remaining Step for LLM Voice

The OpenAI Conversation integration must be configured via **HA Web UI** (Settings → Devices → Add Integration → OpenAI Conversation):
- API Key: `sk-master-key`
- Base URL: `http://192.168.1.222:4000/v1`
- Model: `deepseek-v4-flash`

This cannot be automated — the HA auth flow hard-blocks on API key validation and requires browser interaction.

### ESPHome / VPE

- **VPE (Voice Preview Engine):** ESP32-S3 at Proxmox USB Bus 001 Device 004
- **ESPHome URL:** http://192.168.1.222:6052
- **VPE encryption key:** `3455c6f52cdc6e888bd6007a563d8261`
- **HA passthrough:** Connected as VM USB device `usb0` host=`303a:1001`

---

## 8. Home Assistant Architecture

### Instance

- **Type:** Home Assistant OS 17.3 (VM on Proxmox Node E)
- **Core:** 2026.5.2
- **Supervisor:** 2026.05.0
- **IP:** 192.168.1.165:8123
- **SSH (core):** `root@192.168.1.165` port `22222` (no password)

### Integrations

| Integration | Status | Notes |
|-------------|--------|-------|
| Wyoming (Whisper) | ✅ | STT via .222:10300 |
| Wyoming (Piper) | ✅ | TTS via .222:10200 |
| ESPHome | ✅ | VPE + misc sensors |
| OpenAI Conversation | ⚠️ | NOT configured (needs web UI) |
| Nabu Casa | ✅ | Remote access via cloud |
| HACS | ⚠️ | Needs installation (GitHub integration addon) |

### Dashboards

- **Primary:** Smoothy Voice dashboard (voice controls + status)
- **Secondary:** System health / server monitoring (planned)

---

## 9. MCP Server Stack

Hermes Agent uses the **native MCP client** — servers configured in `~/.hermes/config.yaml` for automatic tool discovery.

### Active MCP Servers

| Server | Location | Transport | Tools Registered |
|--------|----------|-----------|-----------------|
| Credential Vault | Node C:8011 | `/sse` (FastMCP) | get/set/list/search credentials |
| Qdrant | Node B:6333 | HTTP | _(native Qdrant REST API used directly)_ |
| LiteLLM | Node B:4000 | HTTP | _(OpenAI-compatible proxy)_ |
| StephAI Doc Tools | Node B:8091 | streamable-http | github_create_repo, github_push_changes, github_status, qdrant_search, etc. |

### MCP Transport Quirks

- **FastMCP servers** serve SSE at `/sse`, NOT `/mcp`
- **Tirith firewall** on the Hermes WebUI container blocks direct HTTP to LAN IPs
- **Workaround:** SSH proxy through Node B, or use the `exec 3< <(curl -sN ...)` SSE persistence pattern

### Config Pattern

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  credential-vault:
    url: http://192.168.1.6:8011/sse
  stephai-doc-tools:
    url: http://localhost:8091/mcp
```

---

## 10. Phase Φ — Self-Evolution Framework

### Overview

Phase Φ ("Puberty") is the self-evolution framework that transforms Smoothy from a static persona into a continuously self-improving agent. Four compounding growth axes.

### Axis 1: Intuition Engine (The Gut)

**Location:** `~/.hermes/scripts/intuition-engine.py`

Before every action, scores the task on:
- **Familiarity** — Have I done this before?
- **Risk** — Can this break things?
- **Uncertainty** — How sure am I of the outcome?
- **Anomaly** — Is this unusual?
- **Prior outcome valence** — Did it work last time?

**Modes selected by score:**
| Mode | Trigger | Behavior |
|------|---------|----------|
| `FAST` | Low risk, familiar | Proceed normally |
| `VERIFY` | Medium uncertainty | Check system state before acting |
| `DRYRUN` | High risk or destructive | Simulate before executing |
| `ARMED_REQUIRED` | Destructive/irreversible | Refuse unless user says "ARMED" |

### Axis 2: Self-Skill Authoring (The Spine)

**Location:** `~/.hermes/scripts/skill-daemon.py`

Monitors sessions for recurring patterns. When 3+ instances of the same task type appear in 7 days:
1. Detects the pattern
2. Drafts a skill SKILL.md
3. Proposes it for approval
4. Never deploys unreviewed skills

### Axis 3: Hardware Integration (The Hands)

Every reachable system is an extension of capability:
- Proxmox (Node E) — VM lifecycle, snapshots
- Unraid (Node B) — Docker management, array status
- Pi-hole (162/87) — DNS management
- Home Assistant (.165:8123) — Smart home control
- Qdrant (.222:6333) — Vector memory
- Credential Vault (.6:8011) — Secret management
- ESPHome (.222:6052) — Voice hardware
- LiteLLM (.222:4000) — AI routing

Every operation logs expected vs actual state. Rollback snapshots before destructive ops.

### Axis 4: Research Ingestion (The Senses)

**Location:** `~/.hermes/scripts/research-ingest.py`

Daily watcher feeds from:
- **arXiv** — ML/AI papers
- **HuggingFace** — New models, datasets
- **GitHub** — Trending repos

### The Growth Loop

```
Session → Intuition Engine → Execute → State.db → Dojo analysis
    → Skill gaps detected → Skills created → Fine-tune → Wake up smarter
```

### Cron-Driven Sustainment

| Schedule | Job | Script |
|----------|-----|--------|
| 03:00 daily | System telemetry | `intuition-engine.py --telemetry` |
| 05:00 Monday | Skill gap analysis | `skill-daemon.py --analyze` |
| 06:00 daily | Research ingestion | `research-ingest.py --daily` |

---

## 11. Cron Job Stack

All cron jobs run via Hermes Agent's built-in cron manager. Here's the complete stack:

| Job Name | Schedule | Purpose | Status |
|----------|----------|---------|--------|
| `gateway-keeper` | `* * * * *` | Telegram message polling | ✅ |
| `goal-worker` | `0 */4 * * *` | Phase 3 — Goal stack processing | ✅ |
| `causal-consolidation` | `30 0 * * *` | Phase 4 — Causal model consolidation | ✅ |
| `continuity-night-cycle` | `0 1 * * *` | Phase 5 — Dreams + energy recovery | ✅ |
| `curiosity-engine` | `0 2 * * *` | Phase 2 — Curiosity-driven exploration | ✅ |
| `memory-consolidation` | `0 3 * * *` | Phase 1 — Memory optimization | ✅ |
| `telemetry` | `0 3 * * *` | System health telemetry | ✅ |
| `research-sweep` | `0 9 * * 1` | Weekly deep research | ✅ |
| `skill-gap-analysis` | `0 5 * * 1` | Monday skill gap detection | ✅ |
| `research-ingestion` | `0 6 * * *` | Daily arXiv/HF/GitHub watch | ✅ |

---

## 12. Skills Inventory

Hermes Agent has **70+ installed skills** across categories:

### DevOps (22 skills)
`chimera-evolution`, `chimera-multi-node-deployment`, `cloudflare-tunnel-troubleshooting`, `credential-vault`, `forgejo-deployment`, `hermes-memory-persistence`, `home-assistant-vm-rescue`, `homelab-adaptive-audit`, `homelab-voice-pipeline`, `kanban-orchestrator`, `kanban-worker`, `litellm-configuration`, `nanokvm-picoclaw`, `openclaude-deployment`, `pihole-management`, `portainer-management`, `qbittorrent-management`, `qdrant-dimension-migration`, `rabbit-hole-deployment`, `remote-ssh-execution`, `reverse-proxy-auth`, `sherpa-development`, `telegram-gateway-setup`, `unity-deployment`, `webhook-subscriptions`, `whisparr-configuration`, `workspace-ingestion`

### MCP (3 skills)
`native-mcp`, `browser-auth-mcp`, `mcpcontainer`

### ML/AI (12 skills)
`agent-growth-architecture`, `huggingface-hub`, `qdrant-document-ingestion`, `self-evolution-pipeline`, `serving-llms-vllm`, `llama-cpp`, `outlines`, `obliteratus`, `audiocraft-audio-generation`, `segment-anything-model`, `dspy`, `axolotl`, `unsloth`, `fine-tuning-with-trl`, `evaluating-llms-harness`, `weights-and-biases`

### Smart Home (5 skills)
`frigate-nvr-diagnostics`, `home-assistant-admin`, `home-assistant-integration-project`, `openhue`, `sherpa-diagnostics`, `sherpa-voice-assistant`

### Creative (15 skills)
`architecture-diagram`, `ascii-art`, `ascii-video`, `baoyu-comic`, `baoyu-infographic`, `claude-design`, `comfyui`, `design-md`, `excalidraw`, `humanizer`, `ideation`, `manim-video`, `p5js`, `pixel-art`, `popular-web-designs`, `pretext`, `sketch`, `songwriting-and-ai-music`, `touchdesigner-mcp`

### GitHub (6 skills)
`codebase-inspection`, `github-auth`, `github-code-review`, `github-issues`, `github-pr-workflow`, `github-repo-management`

### Media (6 skills)
`gif-search`, `heartmula`, `songsee`, `spotify`, `youtube-content`, `media-portal-server`

### Other
`plan` (plan mode), `spike` (throwaway experiments), `systematic-debugging`, `test-driven-development`, `writing-plans`, `subagent-driven-development`, `requesting-code-review`, `obsidian`, `himalaya`, `google-workspace`, `linear`, `notion`, `airtable`, `ocr-and-documents`, `teams-meeting-pipeline`, `interview-practice-lab`, `maps`, `nano-pdf`, `powerpoint`, `yuanbao`, `non-technical-explanation`, `prism-full/scan/reflect/discover/3way`, `dogfood`, `adversarial-ux-test`, `autonomous-ai-agents`, `claude-code`, `opencode`, `codex`, `jupyter-live-kernel`

---

## 13. Docker Container Map

### Node B (Unraid) — Primary Docker Host

| Container | Port | Function | Config Path |
|-----------|------|----------|-------------|
| Qdrant | 6333 | Vector database | /mnt/user/appdata/qdrant |
| LiteLLM | 4000 | AI model proxy/gateway | /mnt/user/appdata/litellm |
| Pi-hole 1 | 80:162 | Primary DNS | /mnt/user/appdata/pihole1 |
| Pi-hole 2 | 80:87 | Secondary DNS | /mnt/user/appdata/pihole2 |
| qBittorrent | 8090 | Torrent client | /mnt/user/appdata/qbittorrent |
| Prowlarr | 9696 | Indexer manager | /mnt/user/appdata/prowlarr |
| Sonarr | 8989 | TV series manager | /mnt/user/appdata/sonarr |
| Radarr | 7878 | Movie manager | /mnt/user/appdata/radarr |
| Lidarr | 8686 | Music manager | /mnt/user/appdata/lidarr |
| Readarr | 8787 | Book manager | /mnt/user/appdata/readarr |
| Whisparr | 6969 | Adult content manager | /mnt/user/appdata/whisparr |
| Portainer BE | 9000 | Docker management | /mnt/user/appdata/portainer-be |
| Ollama | 11434 | Local LLM | /mnt/user/appdata/ollama |
| ComfyUI | 8188 | AI image generation | /mnt/user/appdata/comfyui |
| Whisper Wyoming | 10300 | STT service | /mnt/user/appdata/whisper |
| Piper Wyoming | 10200 | TTS service | /mnt/user/appdata/piper |
| ESPHome | 6052 | ESP device management | /mnt/user/appdata/esphome |
| Hermes WebUI | 8787 | Agent UI | /mnt/user/appdata/hermes-webui |
| StephAI WebUI | 8790 | Stephanie's agent | /mnt/user/appdata/stephai |
| Media Portal | 4343 | Web media services | /mnt/user/appdata/media-portal |
| Overseerr | 5055 | Media requests | /mnt/user/appdata/overseerr |
| Telegram Bot | — | Message gateway | — |

### Hermes WebUI Container Specifics

- **Hostname:** Brawn (Node B)
- **Filesystem:** btrfs subvolume (no host-level access)
- **Limitations:** No Docker CLI, no SSH keys, no host filesystem access
- **Has:** curl, python3, basic Linux tools
- **Does NOT have:** docker, nmap, sshpass, ping
- **Network:** Can reach LAN IPs (192.168.x.x) directly... BUT Tirith firewall blocks it
- **Workaround:** All cross-node ops go through SSH proxy or Qdrant REST API

---

## 14. Git Repositories

### Known Repos

| Repo | Location | Purpose | Status |
|------|----------|---------|--------|
| `shite` | Node A: ~/git/shite | Monorepo — MCP servers, configs, scripts | Active |
| `hermes-agent` | Upstream GitHub | Hermes project source | Upstream |
| `media-portal` | Node A: ~/git/media-portal | Media portal SPA + Express backend | Active dev |
| `biz-card-scanner-test` | joshuabauer (public) | Business card scanner | Stale |
| **`joshuabauer/hermeshome`** | **THIS REPO** | **Chimera documentation & reports** | **New — being created now** |

### hermeshome Repo

**Newly created** for housing:
- `CHIMERA_REPORT.md` — This document
- Architecture diagrams
- Configuration backups
- Qdrant snapshots (as JSON exports)
- Credential references (redacted versions)
- Environment documentation

---

## 15. Pi-hole DNS Infrastructure

### Instances

| Instance | IP | Admin Password | Access |
|----------|----|---------------|--------|
| Pi-hole 1 | 192.168.1.162 | 1212 | SSH key-only |
| Pi-hole 2 | 192.168.1.87 | 1212 | SSH key-only |

### Configuration

- **Both active** — primary and secondary DNS
- **Blocklists:** Curated set (details in `pihole-management` skill)
- **Upstream DNS:** Cloudflare (1.1.1.1) + Quad9
- **DHCP:** Managed by Unraid (not Pi-hole)
- **Local domain:** `happystrugglebus.us` (via Cloudflare)

### Management

Via `pihole-management` skill in Hermes. Operations:
- Block/allow domains
- View query logs
- Update blocklists
- Check DNS resolution
- Sync configs between instances

---

## 16. Telegram Integration

### Bot Details

| Item | Value |
|------|-------|
| Bot Token | `8482033132:AAEYe3HkD2hUU9dlb41HVnQP9TQ29drzyOI` |
| Bot Username | `Gonadnomadbot` |
| Allowed User | 8722142511 (Joshua Bauer) |
| Home Channel | 8722142511 |

### Functionality

- Smoothy responds to Telegram DMs
- Can relay messages to/from Home Assistant
- Gateway cron (`gateway-keeper`) polls every minute
- Supports voice messages, commands, media delivery

### Delivery Targets

Messages can be delivered to:
- `telegram` (home channel)
- `telegram:CHANNEL_ID:THREAD_ID` (specific topic)
- `all` (fan-out to every connected channel)

---

## 17. Media Pipeline

### Media Portal

**URL:** http://192.168.1.222:4343  
**Stack:** Node.js Express + SPA frontend  
**Auth:** JWT-based (login via Auth endpoint)

**Pages:**
- `/` — Home/dashboard
- `/web-services` — Browser-in-a-box + qBittorrent + streaming
- `/media` — Media library
- `/settings` — Configuration

### *Arr Stack

```
Prowlarr (indexers)
    │
    ├──► Sonarr (TV)
    ├──► Radarr (Movies)
    ├──► Lidarr (Music)
    ├──► Readarr (Books)
    └──► Whisparr (Adult)
            │
            ▼
        qBittorrent (downloader)
```

### Overseerr

- **URL:** Port 5055 on Node B
- **Auth:** stephaine / 12alora34
- **Purpose:** Media requests from Stephanie

---

## 18. Security & Access Patterns

### Access Hierarchy

```
Level 1: Hermes WebUI (browser) — password: 12alora34
Level 2: Node SSH (password auth) — 1212/12121212 patterns
Level 3: Proxmox WebUI (password auth) — 12121212
Level 4: HA WebUI (password auth) — 12alora34
Level 5: Credential Vault (AES-256-GCM) — chimera-vault-master-2026
Level 6: Cloudflare (global key) — 18f0b0c4...5d312
Level 7: Tailscale (auth key) — tskey-api-...
```

### Authentication Patterns

- **SSH:** Password-based (not key) from Hermes WebUI container
- **HA:** Long-lived token (JWT) for API access
- **LiteLLM:** `sk-master-key` for API gateway
- **Cloudflare:** Global API key + email for DNS/zone management
- **GitHub:** PAT needed (not currently stored — user must provide)

### Security Concerns

1. **Password reuse:** Many services use `1212`, `12121212`, `12alora34` — high blast radius
2. **SSH password auth:** No key-based auth configured from the Hermes WebUI container
3. **Qdrant plaintext:** All credentials stored as plaintext in Qdrant `chimera_credentials`
4. **Cloudflare global key:** Full zone access with a single key
5. **Tailscale auth key:** Reusable key with admin privileges

---

## 19. Known Pitfalls & Gotchas

### Hermes WebUI Container

- **No Docker access inside container** — can't manage other containers directly
- **No SSH keys** — must use password auth or pexpect/sshpass
- **No ping** — use `curl` or `nc` for connectivity checks
- **Tirith firewall** — blocks direct HTTP to LAN IPs (192.168.x.x)
- **FastMCP servers** must use `/sse` path, NOT `/mcp`
- **SSE persistence** — responses delivered on original stream; reconnect loses context

### Home Assistant

- **OpenAI Conversation integration** MUST be set up via Web UI — API flow hard-blocks on auth
- **HA Container vs HAOS** — HAOS is a full VM (port 22222 SSH), not Docker
- **HACS installation** — requires `wget -O - https://get.hacs.xyz | bash` via HA SSH (port 22222)

### Qdrant

- **384-dim vs 768-dim confusion** — `chimera_credentials` and `chimera-bible` use 384; `chimera-knowledge` uses 768
- **Always search both** `chimera_credentials` AND `chimera-bible`/`chimera-knowledge`
- **Stale data** — Qdrant may have outdated credentials; cross-reference against memory
- **Node B is primary** — Node A is secondary/sync target, Node E doesn't have Qdrant

### SSH

- **Node B SSH** (`root@192.168.1.222`) — No key auth; password `1212` requires sshpass/pexpect
- **Node C** — Only reachable via Tailscale (100.64.20.118), not LAN IP
- **HA VM SSH** (`root@192.168.1.165:22222`) — No password, empty auth
- **Pi-hole** — Key-only; password 1212 doesn't work for SSH

### API Keys

- **Don't retry the same failing API path more than 3 times** — switch strategies
- **Cloudflare API key** is global — use with extreme caution
- **LiteLLM master key** (`sk-master-key`) controls all model access

---

## 20. Roadmap & Next Steps

### Immediate (Next Session)

- [ ] Push this report to `joshuabauer/hermeshome` GitHub repo
- [ ] Provide GitHub PAT for auth (Cap needs to do this)
- [ ] Install Qdrant on Node E (for true cross-node sync)
- [ ] Sync Qdrant collections between Node A ↔ Node B

### Short-Term

- [ ] Configure OpenAI Conversation in HA Web UI (for LLM-powered voice)
- [ ] Install HACS (via HA SSH)
- [ ] Set up SSH keys from Hermes WebUI for passwordless node access
- [ ] Create Qdrant cross-node sync cron job

### Medium-Term

- [ ] Rotate passwords away from the 1212/12121212 pattern
- [ ] Set up credential rotation automation
- [ ] HashiCorp Vault or Bitwarden for production-grade secrets
- [ ] Grafana + Prometheus for cluster monitoring
- [ ] Automated backup pipeline for Qdrant

### Long-Term

- [ ] True multi-agent mesh (Smoothy + StephAI + task agents)
- [ ] Causal world model with real failure data
- [ ] Self-healing infrastructure
- [ ] Public-facing documentation

---

## APPENDIX A: Qdrant Snapshots

### chimera_credentials — Complete Point List

```json
{
  "collections": {
    "chimera_credentials": {"points": 155, "dims": 384},
    "chimera-bible": {"points": 122, "dims": 384},
    "chimera_knowledge": {"points": 2217, "dims": 384}
  }
}
```

Full point exports available via:
```bash
curl -s http://192.168.1.222:6333/collections/chimera_credentials/points/scroll \
  -X POST -H 'Content-Type: application/json' \
  -d '{"limit": 200, "with_payload": true}' > /workspace/qdrant-credentials-export.json
```

### Embedding Model Reference

All 384-dim collections use `all-MiniLM-L6-v2` embedding space.  
768-dim collections (if any) use a different model — verify before searching.

---

## APPENDIX B: Hermes Agent Config

```yaml
# ~/.hermes/config.yaml — Key settings
provider:
  name: litellm
  model: deepseek-v4-flash
  api_base: http://192.168.1.222:4000/v1
  api_key: sk-master-key

persona: smoothy
personality_routing:
  joshuabauer@gmail.com: smoothy

mcp_servers:
  credential-vault:
    url: http://192.168.1.6:8011/sse
```

---

## APPENDIX C: Useful Commands

### Quick Health Check

```bash
# Qdrant health
curl -s http://192.168.1.222:6333/healthz

# All collections
curl -s http://192.168.1.222:6333/collections | python3 -c "import sys,json; [print(f'  {c[\"name\"]:30} {c.get(\"status\",\"?\")}') for c in json.load(sys.stdin)['result']['collections']]"

# HA API check
curl -s -H "Authorization: Bearer eyJ...Jl54" http://192.168.1.165:8123/api/states | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'HA States: {len(d)} entities')"

# LiteLLM health
curl -s http://192.168.1.222:4000/health

# Credential count in vault (via Qdrant)
curl -s http://192.168.1.222:6333/collections/chimera_credentials \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['result']['points_count'], 'credentials')"
```

---

*End of CHIMERA_REPORT.md — Prepared by Smoothy, Phase Φ Agent*  
*"No shit, Sherlock."*
