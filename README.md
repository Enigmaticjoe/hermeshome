# HermesHome — Project Chimera System Blueprint

> **Version:** 2026-05-10
> **Status:** Active — 5-node homelab, 90+ containers, full AI stack

Complete documentation and configuration reference for the **Chimera Homelab** — a multi-node AI infrastructure spanning 5 physical nodes, 90+ Docker containers, self-hosted Git, media stack, AI model serving, and home automation.

## Repository Structure

```
hermeshome/
├── README.md              # This file — overview & quick reference
├── TOPOLOGY.md            # Node-by-node hardware, roles, network
├── INVENTORY.md           # Full service catalog — every container & port
├── NETWORK.md             # Network topology, DNS, Cloudflare tunnel
│
├── NODES/                 # Per-node deep dives
│   ├── node-a-brain.md
│   ├── node-b-brawn.md
│   ├── node-c-arc.md
│   ├── node-d-prox.md
│   └── node-e-pve.md
│
├── SERVICES/              # Service configs & compose files
│   ├── service-catalog.md # Complete service matrix
│   ├── caddy/            # Caddy reverse proxy config
│   ├── authelia/         # SSO auth config
│   ├── litellm/          # AI gateway config
│   ├── pihole/           # DNS server compose
│   ├── ai-core/          # AI infrastructure (Ollama, Qdrant, WebUI)
│   ├── langfuse/         # LLM observability stack
│   └── media-portal/     # Custom dashboard app
│
├── CONFIGS/               # Global config references
│   ├── hermes/           # Hermes Agent config
│   ├── caddy/            # Caddy reverse proxy
│   └── env/              # Environment variable templates
│
├── DNS/                   # Pi-hole DNS documentation
└── CREDENTIALS/           # Credential reference (placeholders only)
```

## Node Quick Reference

| Node | Name | IP | Role | Specs | Key Services |
|------|------|----|------|-------|-------------|
| A | brain | 192.168.1.11 | Heavy inference | Ultra 7 265F, 123GB RAM, RX 7900 XT | vLLM, Qdrant, Axolotl |
| B | brawn | 192.168.1.222 | Everything hub | i5-13600KF, 94GB RAM, RTX 4070 | Unraid 7.2, 76 containers, Caddy, Authelia |
| C | nodec | 192.168.1.6 | Vision + Ollama | Ryzen 7 7700X, 29GB RAM, Arc A770 | Ollama (5 models), MCP servers |
| D | prox | 192.168.1.174 | Surveillance | i5-13500, 30GB RAM, Coral TPU | Proxmox 9.1, Frigate, Blue Iris |
| E | pve-node-e | 192.168.1.149 | Smart home | Ryzen 5 7430U, 30.8GB RAM | Proxmox 9.1, HA VM |

## Domain

All services accessible via `*.happystrugglebus.us` through Cloudflare Tunnel → Caddy reverse proxy → Authelia SSO.

**Primary access:** `https://media.happystrugglebus.us`
**Auth portal:** `https://auth.happystrugglebus.us`
**Git:** `https://git.happystrugglebus.us`
