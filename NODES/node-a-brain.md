# Node A — Brain (`brain`)

**IP:** 192.168.1.11
**Hostname:** brain
**Role:** Primary compute / AI brain / vector database / homelab orchestration hub

---

## Hardware

| Component | Detail |
|---|---|
| **CPU** | Intel Core Ultra 7 265F (20 cores, 20 threads) |
| **RAM** | 123 GB DDR5 (43 Gi used / 76 Gi free / 79 Gi available) |
| **GPU** | AMD Radeon RX 7900 XT (20 GB VRAM, Navi 31) |
| **OS Disk** | 1.8 TB NVMe (nvme1n1) — `/` ext4, 450 GB used, 1.3 TB free |
| **Scratch Disk** | 931.5 GB NVMe (nvme0n1) — `/srv/scratch` ext4, 2.1 MB used, 870 GB free |
| **SATA HDD 1** | 476.9 GB (sda) — ext4, not mounted |
| **SATA HDD 2** | 3.6 TB (sdb) — ext4, not mounted |
| **SATA SSD** | 21.2 GB (sdc) — btrfs, not mounted |
| **USB NIC** | Yealink WH66 (bus 003), Realtek USB hubs — 10.216.41.100/24 interface (enx1658a7f6622e) |
| **Swap** | 8.0 GB swap file (`/swap.img`) |

### Networking Interfaces

| Interface | Address | Description |
|---|---|---|
| `enp129s0` | 192.168.1.11/24 | Primary LAN (onboard 2.5GbE) |
| `enx1658a7f6622e` | 10.216.41.100/24 | USB Ethernet (IoT/VLAN) |
| `tailscale0` | 100.108.107.123/32 | Tailscale mesh VPN |
| `wlp130s0f0` | — | WiFi (down) |

---

## Operating System

- **OS:** Ubuntu (Linux 7.0.0-15-generic #15-Ubuntu SMP PREEMPT_DYNAMIC)
- **FS:** ext4 on NVMe, CIFS mount for Unraid media share
- **Boot:** UEFI (vfat `/boot/efi`)

---

## Storage

### Local Disks

| Mount | Device | Size | FS | Usage |
|---|---|---|---|---|
| `/` | nvme1n1p2 | 1.8 TB | ext4 | 26% used (450G of 1.8T) |
| `/srv/scratch` | nvme0n1p1 | 916 GB | ext4 | <1% used — AI model scratch / temp |

### SATA (unmounted, available for future use)

| Device | Size | FS | Notes |
|---|---|---|---|
| `/dev/sda1` | 476.9 GB | ext4 | Not mounted |
| `/dev/sdb1` | 3.6 TB | ext4 | Not mounted |
| `/dev/sdc1` | 21.2 GB | btrfs | Not mounted — likely boot/utility SSD |

### Network Mount

```ini
//192.168.1.222/media  →  /mnt/unraid/media  (cifs)
Size: 22 TB total, 1.8 TB used, 21 TB free
Mount options: guest,uid=1000,gid=1000,iocharset=utf8,file_mode=0775,dir_mode=0775,noperm,noatime
Systemd unit: mnt-unraid-media.mount
```

Mounts via systemd `.mount` unit (not fstab), ensuring proper network dependency chain.

---

## Docker Containers

All containers currently running (as of last check):

| Container | Image | Ports | Status |
|---|---|---|---|
| **chimera-qdrant** | qdrant/qdrant:v1.17.1 | 6333-6334 | Up (healthy) |
| **chimera-hub** | sherpa-chimera-hub | — | Up (healthy) |
| **chimera-agno** | chimera-agno:latest | — | Up |
| **rabbit-hole** | rabbit-hole | — | Up |
| **portainer-BE** | portainer/portainer-ee:2.39.1 | 8000, 9000, 9443 | Up |
| **portainer-agent** | portainer/agent:2.27.4 | 9001 | Up |

### Container Details

#### chimera-qdrant
- **Purpose:** Vector database for the homelab AI memory fabric
- **Image:** qdrant/qdrant:v1.17.1
- **Ports:** 6333 (gRPC/REST), 6334 (internal cluster)
- **Collections (4):**
  - `opencode_memory` — OpenCode Web agent memory
  - `chimera_homelab` — Homelab infrastructure knowledge base
  - `rabbit-hole-memory` — Rabbit Hole agent memory
  - `chimera_knowledge` — General knowledge embeddings

#### chimera-hub
- **Purpose:** Central message bus / hub for the Sherpa Chimera multi-agent system
- **Image:** sherpa-chimera-hub
- **Status:** Healthy — all agent connections active

#### chimera-agno
- **Purpose:** Agno AI agent runtime (part of the Chimera multi-agent fabric)
- **Image:** chimera-agno:latest

#### rabbit-hole
- **Purpose:** Rabbit Hole — note-taking / data ingestion agent
- **Image:** rabbit-hole

#### portainer-BE
- **Purpose:** Container management UI (Business Edition)
- **Image:** portainer/portainer-ee:2.39.1
- **Ports:** 8000 (HTTP tunnel), 9000 (Web UI), 9443 (HTTPS)

#### portainer-agent
- **Purpose:** Portainer agent for remote node management
- **Image:** portainer/agent:2.27.4
- **Ports:** 9001

---

## System Services

### Active systemd Services

| Service | Description |
|---|---|
| **nginx.service** | Reverse proxy — serves default on :80, Pi-hole proxy on :8090 |
| **tailscaled.service** | Tailscale mesh VPN node agent |
| **qbittorrent-nox.service** | Torrent client bound to Mullvad VPN interface |
| **kvm-operator.service** | AI-driven KVM/IPMI operator (NanoKVM control) |
| **opencode-web.service** | OpenCode AI coding web server |

### qbittorrent-nox

```ini
Unit: qbittorrent-nox.service
User: jb
Requires: mullvad-daemon.service (VPN must be up first)
After: network-online.target, mullvad-daemon.service, mnt-unraid-media.mount
UMask: 000 (open permissions for media library writes)
```

Torrents download through Mullvad VPN; completed files write directly to the Unraid media share.

### KVM Operator

```ini
Unit: kvm-operator.service
WorkingDir: /home/jb/git/shite/apps/sherpa/kvm-operator
Port: 5000
NanoKVM: http://192.168.1.130
```

AI-powered KVM operator — allows automated remote machine control via NanoKVM hardware at 192.168.1.130.

### OpenCode Web Server

```ini
Unit: opencode-web.service
Port: 4096
User: jb
Command: /usr/bin/opencode web --port 4096 --hostname 0.0.0.0
```

OpenCode Web provides an AI-assisted coding environment accessible via browser.

### Nginx

- **Default server:** Port 80, serves default Nginx page
- **Pi-hole proxy:** Port 8090 — proxies to Pi-hole admin at 192.168.1.222:8081
  - Redirects `/` to `/admin/`

### Tailscale

- **Node name:** brain-1
- **Tailscale IP:** 100.108.107.123
- **Mesh peers:** 13 other nodes in the Tailnet
  - `brawn` (100.79.79.25) — exit node available
  - `jb` (100.67.88.6) — laptop, active direct connection
  - `node-b-unraid` (100.99.104.80) — Unraid server
  - `nodec` (100.100.88.37) — secondary compute
  - `pihole-1` / `pihole-2` — DNS servers
  - `prox` (100.65.215.41) — Proxmox host
  - `tailscale-node` (100.78.103.127) — generic node
  - Several KVM nodes and other devices

---

## GPU & AI Acceleration

### AMD Radeon RX 7900 XT (20 GB)

- **PCI:** Navi 31 at 04:00.0
- **ROCm:** Installed and active — HSA Runtime v1.1, ROCk kernel module loaded
- **Purpose:** vLLM inference acceleration for LLMs
- **vLLM serving:** Port 8000 — model inference API (OpenAI-compatible)
  - Model: Qwen3-14B-AWQ (14B parameter quantized model)
  - Note: vLLM process may be stopped/restarted on demand; port 8000 is reserved for it

### Available Storage for AI Workloads

- `/srv/scratch` — 916 GB NVMe scratch space for model weights, datasets, and temp files
- Large SATA disks available if mounted for additional storage

---

## Network Topology

```
                      Internet
                         |
                    [Mullvad VPN]
                         |
                    qBittorrent-nox
                         |
                  [Tailscale Mesh]
                    /    |    \
                   /     |     \
           brain-1    node-b     nodec
          (this box)  (Unraid)  (compute)
                         |
                  [192.168.1.0/24 LAN]
                    /    |    \
              brain    unraid  nanokvm
            .11       .222     .130
```

### IP Summary

| Network | Address | Purpose |
|---|---|---|
| 192.168.1.0/24 | 192.168.1.11 | Primary LAN |
| 10.216.41.0/24 | 10.216.41.100 | USB Ethernet (secondary network) |
| 100.x.x.x/32 | 100.108.107.123 | Tailscale mesh |

---

## Notes

- **vLLM is configured on port 8000** with ROCm GPU passthrough for inference — may be started/stopped on demand to free GPU memory.
- **SATA disks (sda, sdb, sdc)** are formatted but not currently mounted — available for expansion.
- All Docker containers use bridge networking with port mappings on 192.168.1.11.
- **Chimera Qdrant** houses 4 collections serving the multi-agent fabric's semantic memory.
- **CIFS mount** to Unraid uses guest auth — no credentials stored.
- The **KVM Operator** at port 5000 provides AI-driven remote management of machines via NanoKVM (192.168.1.130).
