# Chimera Homelab — System Blueprint

> Generated: 2026-05-10
> 5 physical nodes, 90+ Docker containers, 44 Cloudflare-tunneled services

---

## Node A — Brain (192.168.1.11)

**Hardware:**
- CPU: Intel Ultra 7 265F
- RAM: 123 GB (43 GB used, 79 GB available)
- Storage: 1.8 TB NVMe root (26% used), 916 GB scratch NVMe (1% used)
- GPU: RX 7900 XT 20 GB (vLLM inference)
- OS: Ubuntu (hostname: `brain`)
- Network: 192.168.1.11/24 (enp129s0), 100.108.107.123 (Tailscale)

**Services (Docker):**
| Container | Image | Port | Notes |
|-----------|-------|------|-------|
| chimera-qdrant | qdrant/qdrant:v1.17.1 | 6333-6334 | Vector DB (standby) |
| chimera-hub | sherpa-chimera-hub | internal | Hub orchestrator |
| chimera-agno | chimera-agno:latest | internal | Agno multi-agent |
| rabbit-hole | rabbit-hole:latest | internal | 3D knowledge graph |
| portainer-BE | portainer-ee:2.39.1 | 8000, 9000 | Docker management |
| portainer-agent | portainer/agent:2.27.4 | 9001 | Portainer edge agent |

**System Services:** vLLM (Qwen3-14B-AWQ), qBittorrent-nox (via Mullvad), Nginx, Tailscale, OpenCode Web Server, KVM Operator, Samba (NFS server for Unraid media mount)

**NFS Mounts:** `//192.168.1.222/media` → `/mnt/unraid/media` (22 TB, 9% used)

---

## Node B — Brawn (192.168.1.222)

**Hardware:**
- CPU: Intel i5-13600KF
- RAM: 94 GB
- GPU: NVIDIA RTX 4070 12 GB (CUDA)
- OS: Unraid 7.2.3 (hostname: `Tower`)
- Storage: 21 TB array (parity 6T + 5 data disks, 19 TB free), 1.8 TB NVMe cache, 907 GB NVMe (Qdrant), 200 GB Docker loop (57 GB used)

**Services (Docker):** 76 containers total

**Media Stack:** Plex, Jellyfin, Stremio, Navidrome, Audiobookshelf, Komga, Kavita, GameVault, Stash

**Arr Stack:** Sonarr, Radarr, Lidarr, Prowlarr, Bazarr, Whisparr, Readarr, Recyclarr, Kometa, Maintainerr, Notifiarr, Recommendarr

**AI Stack:** Ollama (RTX 4070), LiteLLM (:4000), Qdrant (:6333), Hermes WebUI, Langfuse (:3003), Open WebUI, n8n (:5678), Fixie AI

**Infrastructure:** Caddy (reverse proxy), Authelia (SSO), Pi-hole (DNS), Cloudflared (tunnel), Forgejo (Git), Vaultwarden, Portainer BE, Uptime Kuma, Dozzle, Watchtower

**Security:** qBittorrent behind Gluetun (Mullvad VPN), Rclone + Zurg + Riven (debrid stack), Tailscale

---

## Node C — Arc (192.168.1.6)

**Hardware:**
- CPU: AMD Ryzen 7 7700X
- RAM: 29 GB (7.5 GB used, 22 GB available)
- GPU: Intel Arc A770 16 GB (Vulkan/Ollama)
- Storage: 1.8 TB NVMe root (7% used)
- OS: Ubuntu (hostname: `nodec`)
- Network: 192.168.1.6/24 (enp15s0), 100.100.88.37 (Tailscale)

**Docker Containers:** portainer-agent, sherpa-orchestrator, chimera-qdrant

**Ollama Models (Vulkan GPU):**
- qwen3-vl:2b — Vision model
- qwen2.5:7b — General inference
- nous-hermes2:10.7b — Heavy reasoning
- all-minilm:l6-v2 — Embeddings (45 MB)
- moondream — Lightweight vision

**MCP Server Systemd Services:** brothers-keeper, chimera-admin (:8010), mcp-gateway, home-assistant, nanokvm, ollama, pihole, qdrant, unraid (:8009), vllm

---

## Node D — Surveillance (192.168.1.174)

**Hardware:**
- CPU: Intel i5-13500
- RAM: 30 GB (17 GB used)
- Storage: 94 GB root (33% used), 938 GB HDD (bi-archive), 1.9 TB USB (sdd1, 58% used), 464 GB ZFS pool (hdd-pool)
- TPU: Google Coral M.2
- OS: Proxmox 9.1 (hostname: `prox`)

**VMs:**
| VMID | Name | RAM | Boot Disk | Purpose |
|------|------|-----|-----------|---------|
| 100 | blueiris | 8 GB | 527 GB | Camera NVR |
| 101 | frigate | 8 GB | 64 GB | AI object detection (7 cameras, Coral TPU) |

---

## Node E — Smart Home (192.168.1.149)

**Hardware:**
- Device: KAMRUI E3B
- CPU: AMD Ryzen 5 7430U
- RAM: 30.8 GB (4.9 GB used)
- Storage: 68 GB root (9% used), 469 GB data disk (3% used), 31 GB config disk
- OS: Proxmox 9.1 (hostname: `pve-node-e`)

**VMs:**
| VMID | Name | RAM | Boot Disk | Purpose |
|------|------|-----|-----------|---------|
| 100 | haos | 4 GB | 32 GB | Home Assistant OS 2026.4.4 |

**Proxmox Cluster:** 2 nodes — `pve` (local) and `pve-node-e`
