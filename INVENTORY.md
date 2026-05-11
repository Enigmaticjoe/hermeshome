# Service Inventory — Full Container Catalog

> 76 containers on Node B, 6 on Node A, 3 on Node C
> Generated: 2026-05-10

## Node B — 76 Containers

### Media Services
| Service | Port | Image | Auth |
|---------|------|-------|------|
| Plex | :32400 | lscr.io/linuxserver/plex:latest | Plex token |
| Jellyfin | :8096 | lscr.io/linuxserver/jellyfin:latest | Form |
| Stremio | :11470 | stremio/server:latest | None |
| Navidrome | :4533 | deluan/navidrome:latest | Form |
| Audiobookshelf | :13378 | ghcr.io/advplyr/audiobookshelf:latest | Form |
| Komga | :25600 | gotson/komga:latest | Form |
| Kavita | :5000 | jvmilazz0/kavita:latest | Form |
| GameVault | :8998 | phalcode/gamevault-backend:latest | Form |
| Stash | :9998 | stashapp/stash:latest | None |

### *Arr Stack
| Service | Port | Image | Auth |
|---------|------|-------|------|
| Sonarr | :8989 | lscr.io/linuxserver/sonarr:latest | Form |
| Radarr | :7878 | lscr.io/linuxserver/radarr:latest | Form |
| Lidarr | :8686 | lscr.io/linuxserver/lidarr:latest | Form |
| Prowlarr | :9696 | lscr.io/linuxserver/prowlarr:latest | Form |
| Bazarr | :6767 | lscr.io/linuxserver/bazarr:latest | Form |
| Whisparr | :6969 | thespad/whisparr:latest | Form |
| Readarr | :8787 | lscr.io/linuxserver/readarr:latest | Form |
| Maintainerr | :6246 | ghcr.io/maintainerr/maintainerr:latest | None |
| Notifiarr | :5454 | golift/notifiarr:latest | Form |
| Recommendarr | :3006 | tannermiddleton/recommendarr:latest | None |
| Recyclarr | - | ghcr.io/recyclarr/recyclarr:latest | None |
| Kometa | - | kometateam/kometa:latest | None |

### Download Stack
| Service | Port | Image | Notes |
|---------|------|-------|-------|
| qBittorrent | :8090 | lscr.io/linuxserver/qbittorrent:latest | Behind Gluetun VPN |
| Gluetun | various | qmcgaw/gluetun:latest | Mullvad VPN wireguard |
| RDT-Client | :6500 | rogerfar/rdtclient:latest | Real-Debrid |
| Riven | - | ghcr.io/rivenmedia/riven:latest | Debrid manager |
| Riven-Frontend | :3000 | ghcr.io/rivenmedia/riven-frontend:latest | |
| Zurg | :9999 | ghcr.io/debridmediamanager/zurg-testing:latest | Debrid storage |

### AI/ML Stack
| Service | Port | Image | Notes |
|---------|------|-------|-------|
| LiteLLM | :4000 | ghcr.io/berriai/litellm:main-latest | AI gateway (14 models) |
| Ollama | :11434 | ollama/ollama:latest | RTX 4070 GPU |
| Qdrant | :6333-6334 | qdrant/qdrant:latest | Vector DB primary |
| Langfuse | :3003 | ghcr.io/langfuse/langfuse:2 | LLM observability |
| Hermes WebUI | :8787 | ghcr.io/nesquena/hermes-webui:latest | AI agent WebUI |
| Open WebUI | :3001 | ghcr.io/open-webui/open-webui:latest | Chat UI |
| n8n | :5678 | n8nio/n8n:latest | Workflow automation |
| LangGraph Agent | - | langgraph-agent:latest | RAG agent |
| Kokoro TTS | - | kokoro-tts:local | Text-to-speech |

### Infrastructure
| Service | Port | Image | Notes |
|---------|------|-------|-------|
| Caddy | :80 | caddy:alpine | Reverse proxy |
| Authelia | :9091 | authelia/authelia:latest | SSO auth |
| Authelia Redis | - | redis:7-alpine | Session store |
| Cloudflared | - | cloudflare/cloudflared:latest | CF tunnel |
| Pi-hole | :53, :8081 | pihole/pihole:latest | DNS server |
| Forgejo | :3100 | codeberg.org/forgejo/forgejo:8 | Git server |
| Forgejo DB | - | postgres:16-alpine | PostgreSQL |
| Portainer BE | :9000 | portainer/portainer-ee:2.39.1 | Docker mgmt |
| Vaultwarden | - | vaultwarden/server:latest | Password manager |
| Nextcloud | :9443 | lscr.io/linuxserver/nextcloud:latest | Cloud storage |
| Nextcloud DB | - | lscr.io/linuxserver/mariadb:latest | MariaDB |

### Monitoring & Tools
| Service | Port | Image | Notes |
|---------|------|-------|-------|
| Uptime Kuma | :3010 | louislam/uptime-kuma:latest | Uptime monitoring |
| Dozzle | :8888 | amir20/dozzle:latest | Container logs |
| Homepage | :8010 | ghcr.io/gethomepage/homepage:latest | Dashboard |
| SearXNG | :8082 | searxng/searxng:latest | Private search |
| 13ft Ladder | :1313 | ghcr.io/wasi-master/13ft:latest | Paywall bypass |
| Browserless | :32768 | browserless/chrome:latest | Headless browser |
| Jackett | :9117 | lscr.io/linuxserver/jackett:latest | Torrent indexer |
| Tailscale | - | tailscale/tailscale:latest | Mesh VPN |
| Watchtower | - | containrrr/watchtower:latest | Auto-updates |

### MCP Servers (Chimera)
| Service | Image | Function |
|---------|-------|----------|
| mcp-ha | chimera-mcp-servers:latest | Home Assistant |
| mcp-media-stack | chimera-mcp-servers:latest | Media stack control |
| mcp-brothers | chimera-mcp-servers:latest | Task orchestration |
| mcp-pihole | chimera-mcp-servers:latest | Pi-hole control |
| mcp-nanokvm | chimera-mcp-servers:latest | KVM control |
| mcp-vllm | chimera-mcp-servers:latest | vLLM control |
| mcp-ollama | chimera-mcp-servers:latest | Ollama control |
| mcp-qdrant | chimera-mcp-servers:latest | Qdrant control |

### Other
| Service | Notes |
|---------|-------|
| chimera-fileserver | Python file server (:8899) |
| chimera-hub (zealous_cartwright) | Hub instance (:43109) |
| wyoming-piper | Home Assistant TTS |
| wyoming-whisper | Home Assistant STT |
| rclone-zurg | Rclone Zurg mount (:5572) |
| seerr | Overseerr fork (:5055) |
| gamevault-db, riven-db, romm-db | Database backends |
| media-portal | Custom dashboard (:4343) |

## Node A — 6 Containers

| Container | Port | Notes |
|-----------|------|-------|
| chimera-qdrant | :6333-6334 | Vector DB standby |
| chimera-hub | internal | Orchestrator hub |
| chimera-agno | internal | Multi-agent framework |
| rabbit-hole | internal | 3D knowledge graph |
| Portainer BE | :8000, :9000 | Docker management |
| Portainer Agent | :9001 | Edge agent |

## Node C — 3 Containers

| Container | Notes |
|-----------|-------|
| portainer-agent | Portainer edge agent |
| sherpa-orchestrator | Voice assistant orchestrator |
| chimera-qdrant | Vector DB (warm standby) |
