# Chimera Network Topology

> All nodes on 192.168.1.0/24 LAN (VLAN 1, flat network)
> Cloudflare Tunnel provides external access

## LAN Layout

```
Internet
    │
    ▼
Cloudflare (TLS termination)
    │
    ▼  (Tunnel)
cloudflared-fix (Node B Docker)
    │
    ▼  (:80 origin)
Caddy (Node B, localhost:80)
    │
    ├── auth.happystrugglebus.us ───── Authelia (:9091)
    │
    ├── *.happystrugglebus.us ──────── forward_auth → Authelia → service
    │
    └── (direct) ───────────────────── stash, debug, downloads
```

## Node Connectivity

| From → To | Protocol | Method | Latency |
|-----------|----------|--------|---------|
| A → B | LAN | Direct | 0.4 ms |
| A → C | LAN | Direct | 0.7 ms |
| A → D | LAN | Direct | 0.3 ms |
| A → E | LAN | Direct | 0.7 ms |
| B/C → Any | LAN | Direct | sub-1ms |
| Any → Any | WAN | Tailscale | 100.100.x.x/32 |

## IP Assignments

| Node | LAN IP | Tailscale IP | Subnet |
|------|--------|-------------|--------|
| A (brain) | 192.168.1.11 | 100.108.107.123 | /24 |
| B (brawn) | 192.168.1.222 | 100.79.79.25 | /24 |
| C (nodec) | 192.168.1.6 | 100.100.88.37 | /24 |
| D (prox) | 192.168.1.174 | 100.65.215.41 | /24 |
| E (pve-node-e) | 192.168.1.149 | none | /24 |

**Additional IPs:** Node A also has 10.216.41.100/24 (USB NIC), Node C has 10.151.169.100/24 (USB NIC)

## DNS

**Primary DNS:** Pi-hole on Node B (192.168.1.222:53)
**Secondary DNS:** Pi-hole secondary (TBD)
**Upstream:** Cloudflare 1.1.1.1 / 1.0.0.1
**Domain:** `*.happystrugglebus.us` → Cloudflare → tunnel → Caddy

All internal services resolve via Cloudflare DNS proxied through the tunnel. Direct LAN access uses IP:port.

## Cloudflare Tunnel

**Method:** cloudflared Docker container (cloudflared-fix) on Node B
**Mode:** Token-based (not config.yml)
**Protocol:** HTTP/2
**Ingress:** Managed via Cloudflare API v51
**Auth:** CF_ACCOUNT_ID + CF_API_TOKEN in environment

## Reverse Proxy (Caddy)

**Location:** Node B Docker, caddy:alpine
**Port:** :80 (origin HTTP)
**TLS:** Terminated by Cloudflare at edge

All services behind Authelia `forward_auth` except:
- `auth.happystrugglebus.us` — Authelia portal (bypass)
- `stash.happystrugglebus.us` — No auth (API access)
- `debug.happystrugglebus.us` — Diagnostic endpoint
- `downloads.happystrugglebus.us` — File server
