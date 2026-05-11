# Node C — `nodec` (Arc GPU Workstation)

**Hostname:** nodec
**Designation:** Node C — GPU compute & MCP orchestration node
**Role:** Multi-purpose workstation running Ollama (LLM inference), Qdrant (vector DB), Sherpa orchestrator, and 10 MCP systemd servers. Primary GPU compute node using the Intel Arc A770 16GB for Vulkan-based inference.

---

## Hardware Specifications

| Component | Detail |
|-----------|--------|
| **CPU** | AMD Ryzen 7 7700 (8 cores, 16 threads) |
| **RAM** | 29 GiB total (7.5 GiB used / 21 GiB free) |
| **Swap** | 22 GiB (6.4 GiB used / 16 GiB free) |
| **GPU (Discrete)** | Intel Arc A770 16GB (DG2) — Vulkan via Mesa 26.0.3 open-source driver |
| **GPU (Integrated)** | AMD Radeon Raphael (RADV) — iGPU on Ryzen 7 7700 |
| **Storage** | 1.8 TB NVMe (`/dev/nvme1n1p2`) — 7% used (119 GiB used, 1.6 TiB available) |
| **Motherboard/BIOS** | AM5 platform (Ryzen 7000 series) |

### GPU Details — Intel Arc A770

- **Vendor:** Intel Corporation (0x8086)
- **Device:** DG2 [Arc A770] (0x56a0)
- **Type:** Discrete GPU (PHYSICAL_DEVICE_TYPE_DISCRETE_GPU)
- **VRAM:** 16 GB GDDR6
- **Driver:** Intel open-source Mesa driver (Mesa 26.0.3-1ubuntu1)
- **Vulkan API:** 1.4.335 (conformance version 1.4.0.0)
- **Driver Version:** 26.0.3
- **DRM Devices:** `/dev/dri/card0`, `/dev/dri/card1`, `/dev/dri/renderD128`, `/dev/dri/renderD129`

The Arc A770 provides Vulkan compute capability used for LLM inference via Ollama and other GPU-accelerated workloads. The integrated AMD Raphael GPU is also available but unused for compute tasks.

---

## Software & OS

| Layer | Version |
|-------|---------|
| **OS** | Ubuntu 26.04 LTS (Resolute Raccoon) |
| **Kernel** | 7.0.0-14-generic #14-Ubuntu SMP PREEMPT_DYNAMIC |
| **Container Runtime** | Docker (via Portainer agent) |
| **LLM Runtime** | Ollama (systemd service, bare metal — NOT containerized) |
| **Vector DB** | Qdrant (Docker container `chimera-qdrant`) |

---

## Network Interfaces

| Interface | IP Address | Subnet | Purpose |
|-----------|------------|--------|---------|
| **enp15s0** | `192.168.1.6` | `/24` | Main LAN — primary connectivity |
| **enxa655ee9461f8** | `10.151.169.100` | `/24` | USB Ethernet — management/aux network |
| **tailscale0** | `100.100.88.37` | `/32` | Tailscale mesh VPN — secure inter-node access |
| **docker0** | `172.17.0.1` | `/16` | Default Docker bridge |
| **docker_gwbridge** | `172.19.0.1` | `/16` | Docker overlay/gateway bridge |

### IP Summary

- `192.168.1.6` — LAN (primary)
- `10.151.169.100` — USB NIC
- `100.100.88.37` — Tailscale

---

## Docker Containers

All running via Docker (bare engine, not Portainer-managed stacks):

| Container | Image | Status |
|-----------|-------|--------|
| **portainer-agent** | `portainer/agent:2.27.4` | Up (Portainer management agent for cluster visibility) |
| **sherpa-orchestrator** | `sherpa2:latest` | Up (Multi-agent orchestration engine) |
| **chimera-qdrant** | `qdrant/qdrant:latest` | Up (Vector database — Chimera knowledge memory) |

Note: Docker networks are present at `172.17.0.0/16` and `172.19.0.0/16`, supporting bridge and overlay connectivity.

---

## Ollama — LLM Inference (Bare Metal)

Ollama runs as a **systemd service** (not containerized) for direct GPU access via Vulkan.

### Installed Models

| Model | Size | Purpose |
|-------|------|---------|
| **qwen3-vl:2b** | 1.9 GB | Vision-language — multimodal inference |
| **qwen2.5:7b** | 4.7 GB | General-purpose LLM — chat & completion |
| **nous-hermes2:10.7b** | 6.1 GB | High-quality instruct model (Nous Research) |
| **all-minilm:l6-v2** | 45 MB | Embeddings — semantic search & vectorization |
| **moondream** | 1.7 GB | Lightweight vision-language model |

### Ollama Service Details

- **Type:** systemd unit (`ollama.service`)
- **GPU Backend:** Vulkan (Intel Arc A770 via Mesa Intel driver)
- **Status:** active (running)
- **API:** Default Ollama HTTP API (localhost:11434)

---

## MCP Servers (systemd Services)

Ten MCP (Model Context Protocol) servers run as systemd services on Node C. These are the service endpoints that enable agent-to-system communication across the Chimera Neural Fabric.

| Service Name | Description |
|-------------|-------------|
| **mcp-brothers-keeper** | Brothers Keeper — multi-agent task orchestration & agent registry |
| **mcp-chimera-admin** | Chimera Admin Server (:8010) — system administration, SSH exec, Qdrant queries |
| **mcp-gateway** | MCP Web Gateway (Hermes-tuned) — external HTTP/MCP bridge |
| **mcp-home-assistant** | Home Assistant integration — smart home entity control & monitoring |
| **mcp-nanokvm** | NanoKVM remote KVM control — BIOS-level remote management |
| **mcp-ollama** | Ollama MCP bridge — LLM chat, generation, vision analysis via Ollama |
| **mcp-pihole** | Pi-hole MCP — DNS filtering control, query stats, gravity management |
| **mcp-qdrant** | Qdrant MCP — vector DB operations, semantic search, memory queries |
| **mcp-unraid** | Unraid Server (:8009) — Unraid NAS management, Docker, disks, VMs |
| **mcp-vllm** | vLLM MCP server — large model inference via vLLM backend |

### MCP Architecture Notes

All MCP servers are **systemd-managed** for reliability and automatic restart. They communicate via the MCP protocol (stdin/stdout JSON-RPC for local services, HTTP for remote services like chimera-admin:8010 and unraid:8009). This node acts as the **primary MCP service host** in the Chimera Neural Fabric, concentating 10 of the fabric's service endpoints.

---

## Role in the Chimera Neural Fabric

Node C fills several critical roles:

1. **GPU Inference Node** — The Intel Arc A770 provides Vulkan compute for on-prem LLM inference, vision processing, and embeddings generation. This is the only node in the fabric with a discrete consumer GPU.

2. **MCP Service Hub** — Hosts 10 MCP servers covering infrastructure (Brothers Keeper, Qdrant, Unraid), AI (Ollama, vLLM), smart home (Home Assistant), network (Pi-hole), and remote management (NanoKVM).

3. **Orchestration Engine** — Runs the Sherpa orchestrator for coordinating multi-agent tasks across the fabric.

4. **Vector Database Host** — Qdrant stores Chimera's semantic memory, homelab knowledge base, and agent context for retrieval-augmented generation (RAG).

---

## Access & Connectivity

| Method | Target |
|--------|--------|
| **SSH** | `192.168.1.6` (LAN), `100.100.88.37` (Tailscale) |
| **Ollama API** | `http://192.168.1.6:11434` |
| **Qdrant API** | `http://192.168.1.6:6333` |
| **Portainer Agent** | `http://192.168.1.6:9001` |
| **Chimera Admin** | `http://192.168.1.6:8010` |
| **Unraid MCP** | `http://192.168.1.6:8009` |

---

## Notes

- CPU model detected as "AMD Ryzen 7 7700 8-Core Processor" — believed to be a Ryzen 7 7700X based on hardware context (29GB RAM, AM5 platform), but `lscpu` reports the non-X variant string.
- The Arc A770's 16GB VRAM makes it suitable for running 7B-10B parameter models at reasonable quantization levels via Ollama's Vulkan backend.
- No NVIDIA GPU is present on this node; all GPU compute is via Intel Mesa/Vulkan or AMD integrated graphics.
- Uptime at time of documentation: 2 days (clean boot).
- Load average: 3.00 (idle-ish, some background processes).
