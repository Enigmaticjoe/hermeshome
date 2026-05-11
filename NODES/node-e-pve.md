# Node E — pve-node-e (Smart Home)

> **IP:** 192.168.1.149 | **Tailscale:** none
> **OS:** Proxmox 9.1 (pve-manager/9.1.1, kernel 6.17.2-1-pve)
> **Hardware:** KAMRUI E3B mini PC

## Hardware

- **CPU:** AMD Ryzen 5 7430U
- **RAM:** 30.8 GB (4.9 GB used, 25 GB available)
- **Storage:**
  - 68 GB root LVM (9% used)
  - 469 GB SSD at /mnt/proxmox-data (3% used)
  - 31 GB config disk at /mnt/ha-config (23% used)
- **Swap:** 8 GB (0 used)

## VMs

| VMID | Name | RAM | Boot Disk | Status |
|------|------|-----|-----------|--------|
| 100 | haos | 4 GB | 32 GB | Running |

### Home Assistant VM (100)

- **OS:** Home Assistant OS 2026.4.4
- **IP:** 192.168.1.165:8123
- **Resources:** 4 cores, 4 GB RAM
- **Features:**
  - 645+ entities across 263 components
  - Voice pipelines: Whisper (STT) + Piper (TTS)
  - Zigbee2MQTT, Z-Wave JS, ESPHome
  - Mosquitto MQTT broker
  - Chimera Command dashboard integration
  - Assist voice satellite paired

## Storage Layout

| Storage ID | Type | Path | Content |
|------------|------|------|---------|
| local | dir | /var/lib/vz | Templates, backup, ISO |
| local-lvm | LVM-thin | pve/data | VM images, rootdir |
| proxmox-data | dir | /mnt/proxmox-data | VM images, backup, templates |

## Network

- **vmbr0:** 192.168.1.149/24 (LAN bridge)
- No Tailscale (HA VM handles external access)

## Proxmox Cluster

- 2 nodes registered: `pve` and `pve-node-e`
- No ZFS — traditional LVM/ext4 storage
