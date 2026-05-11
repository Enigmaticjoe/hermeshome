# Node B — Brawn (192.168.1.222)

> Hostname: `Tower` | OS: Unraid 7.2.3 | Role: Data + GPU compute + media + AI infrastructure
> Generated: 2026-05-10 22:43 UTC

---

## Hardware

| Component | Spec |
|-----------|------|
| CPU | Intel Core i5-13600KF (20 threads, 13th Gen) |
| RAM | 94 GB (19 GB used, 74 GB available — no swap) |
| GPU | NVIDIA RTX 4070 12 GB GDDR6X (CUDA) — idle 39 C, 0% utilization, 4.5 W draw |
| Motherboard | Unknown (Unraid host) |
| Network | 192.168.1.222/24 (br0), 100.99.104.80 (Tailscale1), 100.79.79.25 (Tailscale0, idle, offers exit node) |
| Bonding | Active-backup, eth0 primary — 1 GbE |

### Storage Topology

| Mount | Device | Size | Used | Free | Notes |
|-------|--------|------|------|------|-------|
| /mnt/user (shfs) | Array (6 disks) | 21 TB | 1.3 TB | 19 TB | 7% used |
| /mnt/disk1 | /dev/md1p1 | 5.5 TB | 947 GB | 4.6 TB | Parity: 6 TB |
| /mnt/disk2 | /dev/md2p1 | 3.7 TB | 72 GB | 3.6 TB | |
| /mnt/disk3 | /dev/md3p1 | 3.7 TB | 72 GB | 3.6 TB | |
| /mnt/disk4 | /dev/md4p1 | 3.7 TB | 72 GB | 3.6 TB | |
| /mnt/disk6 | /dev/md6p1 | 3.7 TB | 72 GB | 3.6 TB | |
| /mnt/cache | /dev/nvme0n1p1 | 1.8 TB | 483 GB | 1.3 TB | NVMe cache pool (28% used) |
| /mnt/qdrant | /dev/nvme1n1p3 | 907 GB | 56 KB | 861 GB | Dedicated NVMe for Qdrant |
| /mnt/aux | /dev/nvme2n1p2 | 239 GB | 405 MB | 239 GB | Auxiliary NVMe (1% used) |

**Parity:** Parity disk is 6 TB. Last parity check completed Apr 5, 2026 — 40,539 seconds, 148 GB corrected, 0 errors. Regular monthly checks.

**Array Status:** Started, 6 disks, resync action=check P (parity check). Last resync completed with 0 corrections.

### Docker Storage

| Volume | Size | Purpose |
|--------|------|---------|
| Docker loop image | 200 GB | Docker overlay storage |

---

## Container Inventory — 76 Docker Containers

### 1. Media Stack

| Container | Port | Image | Uptime | Notes |
|-----------|------|-------|--------|-------|
| plex | 32400 | lscr.io/linuxserver/plex:latest | 5 days | Primary media server, 520 MB |
| jellyfin | 8096 | lscr.io/linuxserver/jellyfin:latest | 4 days | FOSS alternative, 288 MB |
| stremio-server | 11470 | stremio/server:latest | 4 days | Torrent streaming, 103 MB |
| navidrome | 4533 | deluan/navidrome:latest | 2 days | Music streaming, 26 MB |
| audiobookshelf | 13378 | ghcr.io/advplyr/audiobookshelf:latest | 5 days | Audiobook/podcast server, 78 MB |
| komga | 25600 | gotson/komga:latest | 5 days | Comic/Manga server, 739 MB (largest media app) |
| kavita | 5000 | jvmilazz0/kavita:latest | 5 days | Manga/ebook reader, 311 MB (healthy) |
| gamevault | 8998 | phalcode/gamevault-backend:latest | 5 days | Game library manager, 143 MB (healthy) |
| stash | 9998 | stashapp/stash:latest | 5 days | Adult media library, 106 MB |

### 2. *Arr Stack (Media Management)

| Container | Port | Image | Uptime | Notes |
|-----------|------|-------|--------|-------|
| sonarr | 8989 | lscr.io/linuxserver/sonarr:latest | 43h | TV series management, 227 MB |
| radarr | 7878 | lscr.io/linuxserver/radarr:latest | 3 days | Movie management, 215 MB |
| lidarr | 8686 | lscr.io/linuxserver/lidarr:latest | 2 days | Music management, 174 MB |
| prowlarr | 9696 | lscr.io/linuxserver/prowlarr:latest | 3 days | Indexer manager, 209 MB |
| bazarr | 6767 | lscr.io/linuxserver/bazarr:latest | 2 days | Subtitle management, 195 MB |
| whisparr | 6969 | thespad/whisparr:latest | 2 days | Adult content manager, 236 MB |
| maintainerr | 6246 | ghcr.io/maintainerr/maintainerr:latest | 43h | Media maintenance, 209 MB |
| notifiarr | 5454 | golift/notifiarr:latest | 5 days | Discord/notification gateway, 34 MB |
| recommendarr | 3006 | tannermiddleton/recommendarr:latest | 5 days | Recommendation engine (healthy), 47 MB |
| recyclarr | — | ghcr.io/recyclarr/recyclarr:latest | 5 days | Radarr/Sonarr config sync, 36 MB |
| kometa | — | kometateam/kometa:latest | 5 days | Plex metadata manager, 61 MB |

### 3. Download & Debrid Stack

| Container | Port | Image | Uptime | Notes |
|-----------|------|-------|--------|-------|
| qbittorrent | 8090 | lscr.io/linuxserver/qbittorrent:latest | 19h | Torrent client behind Gluetun, 29 MB |
| gluetun | — | qmcgaw/gluetun:latest | 19h | Mullvad WireGuard VPN (healthy), 100 MB |
| rdt-client | 6500 | rogerfar/rdtclient:latest | 2 days | Real-Debrid API client (healthy), 180 MB |
| riven | — | ghcr.io/rivenmedia/riven:latest | 5 days | Debrid media manager, 170 MB |
| riven-frontend | 3000 | ghcr.io/rivenmedia/riven-frontend:latest | 5 days | Riven web UI, 35 MB |
| zurg | 9999 | ghcr.io/debridmediamanager/zurg-testing:latest | 5 days | Debrid virtual filesystem (healthy), 50 MB |
| rclone-zurg | 5572 | rclone/rclone:latest | 43h | Rclone mount for Zurg, 102 MB |
| riven-db | — | postgres:17-alpine | 5 days | Riven PostgreSQL (healthy), 63 MB |
| jackett | 9117 | lscr.io/linuxserver/jackett:latest | 12h | Torrent indexer proxy, 107 MB |

### 4. AI/ML Stack

| Container | Port | Image | Uptime | RAM | Notes |
|-----------|------|-------|--------|-----|-------|
| chimera-ollama | 11434 | ollama/ollama:latest | 42h | 593 MB | GPU-accelerated (RTX 4070) |
| litellm_gateway | 4000 | ghcr.io/berriai/litellm:main-latest | 11h | 539 MB | OpenAI-compatible AI gateway, 14 model routes |
| chimera-qdrant | 6333-6334 | qdrant/qdrant:latest | 43h | 1.13 GB | Primary vector DB (healthy), dedicated NVMe |
| langfuse | 3003 | ghcr.io/langfuse/langfuse:2 | 3 days | 306 MB | LLM observability & tracing |
| langfuse-db | — | postgres:17-alpine | 3 days | 66 MB | Langfuse PostgreSQL backend (healthy) |
| hermes-webui | 8787 | ghcr.io/nesquena/hermes-webui:latest | 19h | 544 MB | AI agent Web UI (healthy) |
| n8n | 5678 | n8nio/n8n:latest | 2 days | 373 MB | Workflow automation engine |
| langgraph-agent | — | langgraph-agent:latest | 5 days | 48 MB | LangGraph RAG agent |
| kokoro-tts | — | kokoro-tts:local | 5 days | 207 MB | Local text-to-speech (Japanese+English) |
| mcp-vllm | — | chimera-mcp-servers:latest | 5 days | 73 MB | vLLM MCP control |
| mcp-ollama | — | chimera-mcp-servers:latest | 5 days | 73 MB | Ollama MCP control |
| mcp-qdrant | — | chimera-mcp-servers:latest | 5 days | 75 MB | Qdrant MCP control |

### 5. Infrastructure (Networking, Auth, Storage)

| Container | Port | Image | Uptime | Notes |
|-----------|------|-------|--------|-------|
| caddy | 80, 443 | caddy:alpine | 10h | Reverse proxy (all services) |
| authelia | 9091 | authelia/authelia:latest | 2 days | SSO/2FA auth portal (healthy) |
| authelia-redis | — | redis:7-alpine | 2 days | Authelia session store, 8.5 MB |
| pihole | 53, 8081 | pihole/pihole:latest | 5 days | DNS server + ad blocking (healthy), 173 MB |
| cloudflared-fix | — | cloudflare/cloudflared:latest | 46h | Cloudflare Tunnel (fix variant), 41 MB |
| tailscale | — | tailscale/tailscale:latest | 5 days | Mesh VPN, 128 MB, offers exit node |
| forgejo | 3100 | codeberg.org/forgejo/forgejo:8 | 5 days | Git server (Gitea fork), 439 MB |
| forgejo-db | — | postgres:16-alpine | 5 days | Forgejo PostgreSQL backend, 44 MB |
| portainer_agent | 9001 | portainer/agent:2.27.4 | 5 days | Portainer edge agent, 43 MB |
| Portainer-BE | 9000 | portainer/portainer-ee:2.39.1 | 5 days | Docker management UI, 101 MB |
| vaultwarden | — | vaultwarden/server:latest | 5 days | Bitwarden-compatible password vault (healthy), 40 MB |
| nextcloud | 9443 | lscr.io/linuxserver/nextcloud:latest | 3 days | Cloud file sync, 230 MB |
| nextcloud-db | — | lscr.io/linuxserver/mariadb:latest | 4 days | Nextcloud MariaDB backend, 80 MB |
| chimera-fileserver | 8899 | python:3.12-alpine | 10h | Python HTTP file server, 13 MB |
| chimera-hub (zealous_cartwright) | — | chimera-hub:latest | 3 days | Hub orchestrator instance, 50 MB |

### 6. Monitoring & Utility

| Container | Port | Image | Uptime | Notes |
|-----------|------|-------|--------|-------|
| uptime-kuma | 3010 | louislam/uptime-kuma:latest | 5 days | Uptime monitoring dashboard (healthy), 156 MB |
| dozzle | 8888 | amir20/dozzle:latest | 4 days | Real-time container log viewer, 36 MB |
| homepage | 8010 | ghcr.io/gethomepage/homepage:latest | 43h | Custom homelab dashboard (healthy), 156 MB |
| searxng | 8082 | searxng/searxng:latest | 43h | Private meta-search engine, 129 MB |
| 13ft-ladder | 1313 | ghcr.io/wasi-master/13ft:latest | 5 days | Paywall/article bypass, 31 MB |
| browserless | 32768 | browserless/chrome:latest | 5 days | Headless browser automation, 120 MB |
| watchtower | — | containrrr/watchtower:latest | 5 days | Auto-container updates (healthy) |
| media-portal | 4343 | media-portal:latest | 37 min | Custom media dashboard, 41 MB |
| seerr | 5055 | ghcr.io/seerr-team/seerr:latest | 5 days | Media request portal (Overseerr fork), 229 MB |
| tautulli | — | lscr.io/linuxserver/tautulli:latest | 4 days | Plex usage/analytics, 95 MB |
| recyclarr | — | ghcr.io/recyclarr/recyclarr:latest | 5 days | Quality profile sync, 36 MB |

### 7. Home Assistant Voice (Wyoming)

| Container | Image | Uptime | Notes |
|-----------|-------|--------|-------|
| wyoming-piper | rhasspy/wyoming-piper:latest | 4 days | Local TTS, 39 MB |
| wyoming-whisper | rhasspy/wyoming-whisper:latest | 4 days | Local STT, 466 MB |

### 8. Gaming/ROMs

| Container | Port | Image | Uptime | Notes |
|-----------|------|-------|--------|-------|
| gamevault | 8998 | phalcode/gamevault-backend:latest | 5 days | Game library (healthy), 143 MB |
| gamevault-db | — | postgres:16-alpine | 5 days | GameVault PostgreSQL, 33 MB |
| romm-db | — | mariadb:10 | 5 days | ROM manager DB, 110 MB |

### 9. MCP Server Ecosystem (Chimera)

All MCP servers run as separate containers from the `chimera-mcp-servers:latest` image. Each is ~73-82 MB.

| Container | Function |
|-----------|----------|
| mcp-ha | Home Assistant control via SSH |
| mcp-media-stack | Media stack operations |
| mcp-brothers | Multi-agent task orchestration |
| mcp-pihole | Pi-hole DNS management |
| mcp-nanokvm | KVM over IP control |
| mcp-vllm | vLLM inference control |
| mcp-ollama | Ollama control |
| mcp-qdrant | Qdrant vector DB control |

### 10. Other

| Container | Notes |
|-----------|-------|
| rabbit-hole | 3D knowledge graph explorer, 63 MB, 4 days uptime |
| rclone-zurg | Rclone mount for Zurg RDebrid, 102 MB |

---

## Share Layout

| Share | Path | Size | Purpose |
|-------|------|------|---------|
| media | /mnt/user/media/ | 16 TB | Movies, TV, music, books, games |
| appdata | /mnt/user/appdata/ | 309 GB | Docker config volumes |
| system | /mnt/user/system/ | 169 GB | Unraid system + Docker image |
| NodaDocs | /mnt/user/NodaDocs/ | 5.9 GB | Homelab documentation |
| data | /mnt/user/data/ | 1.1 GB | Misc data |
| nextcloud | /mnt/user/nextcloud/ | 69 MB | NC instance data |
| docker | /mnt/user/docker/ | 46 MB | Docker compose files |
| nextcloud_data | /mnt/user/nextcloud_data/ | 1.1 MB | NC user files |
| hope, DUMB, storage, snapshots, realdebrid, mounts, downloads, vaultwarden, swap, josh, backups, ai_media, cloud | various | < 1 MB each | Misc/service-specific shares |

---

## Networking

### IP Addresses

| Interface | Address | Scope |
|-----------|---------|-------|
| br0 | 192.168.1.222/24 | LAN (primary) |
| shim-br0 | 192.168.1.222/24 | Unraid bridge shim |
| tailscale0 | 100.79.79.25/32 | Tailscale (brawn) |
| tailscale1 | 100.99.104.80/32 | Tailscale (node-b-unraid) |
| docker0 | 172.17.0.1/16 | Default Docker bridge |
| docker_gwbridge | 172.20.0.1/16 | Docker gateway |
| Plus 10 custom Docker bridge networks | 172.18-172.31.x | Isolated container networks |

### Tailscale Peers

| Peer | Address | Status |
|------|---------|--------|
| brain-1 (Node A) | 100.108.107.123 | Connected |
| brawn (self) | 100.79.79.25 | Idle, offers exit node |
| jb | 100.67.88.6 | Connected |
| nodec | 100.100.88.37 | Connected |
| pihole-1 | 100.104.139.38 | Connected |
| pihole-2 | 100.73.184.1 | Connected |
| prox (Node D) | 100.65.215.41 | Connected |
| tailscale-node | 100.78.103.127 | Connected |
| kvm-97a9 | 100.80.243.78 | Connected |
| homeassistant | 100.110.38.37 | Offline (1 day ago) |
| lappy | 100.106.70.46 | Offline (20h ago) |
| node-a-kvm | 100.99.133.29 | Offline (4 days ago) |
| kvm-ec10 | 100.95.17.92 | Offline (19 days ago) |

### Bonding

- Mode: Active-backup (fault-tolerance)
- Active slave: eth0
- Status: Up, MII polling 100ms

---

## Key Service Dependencies

```
Cloudflare (Internet)
  -> Cloudflared (Node B)
    -> Caddy (Node B, reverse proxy)
      -> Authelia (SSO)
        -> Forgejo | Nextcloud | Vaultwarden | Hermes WebUI | etc.

Pi-hole (DNS)
  -> All LAN DNS queries

Tailscale (Mesh VPN)
  -> Node A (Brain) | Node C (Arc) | Node D/E | Clients

Qdrant (Primary Vector DB) — Node B
  -> LiteLLM | Langfuse | n8n | LangGraph | Hermes WebUI
  -> Replicated to Node A (standby) and Node C (warm standby)

Ollama (GPU) — Node B
  -> LiteLLM | Hermes WebUI | n8n | LangGraph

Gluetun (Mullvad VPN)
  -> qBittorrent (torrent download isolation)
```

---

## Performance Notes

- CPU load average: 0.27 / 0.29 / 0.27 (extremely idle, 20 threads)
- Memory: 19 GB / 94 GB used (20%) — heavy containers: Qdrant 1.13 GB, Ollama 593 MB, LiteLLM 539 MB, Hermes WebUI 544 MB, Plex 520 MB, Komga 739 MB, Forgejo 439 MB, n8n 373 MB
- GPU: RTX 4070 idle at 39 C, 0% util, 4.5 W — ready for inference
- Total container memory: ~13 GB across 76 containers
- No swap configured (0B)

## Authelia SSO-Protected Services

All externally-facing services are routed through Caddy -> Authelia for authentication. This includes: Forgejo, Nextcloud, Vaultwarden, Hermes WebUI, n8n, Langfuse, Uptime Kuma, Dozzle, Homepage, Kavita, Audiobookshelf, Komga, GameVault, Seerr, Navidrome, and more.

## Backup Strategy

- appdata contains all Docker container configurations (309 GB)
- Unraid parity provides RAID-like protection for the array
- Frequencies: Watchtower manages container image updates
- Unraid parity checks run monthly (last: Apr 5, 2026, clean)
- No off-site backup configured (notable gap)
