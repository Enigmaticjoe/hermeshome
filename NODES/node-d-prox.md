# Node D — prox (Surveillance)

> **IP:** 192.168.1.174 | **Tailscale:** 100.65.215.41
> **OS:** Proxmox 9.1 (pve-manager/9.1.6, kernel 6.17.13-1-pve)

## Hardware

- **CPU:** Intel i5-13500
- **RAM:** 30 GB (17 GB used, 12 GB available)
- **Storage:**
  - 94 GB root (LVM, 33% used)
  - 938 GB HDD at /mnt/pve/bi-archive (36% used) — Blue Iris archive
  - 1.9 TB USB HDD at /mnt/pve/sdd1 (58% used) — Frigate recordings
  - 464 GB ZFS pool "hdd-pool" (325 GB allocated)
- **TPU:** Google Coral M.2 (Frigate AI detection)
- **Swap:** 8 GB (770 MB used)

## VMs

| VMID | Name | RAM | Boot Disk | Status |
|------|------|-----|-----------|--------|
| 100 | blueiris | 8 GB | 527 GB | Running |
| 101 | frigate | 8 GB | 64 GB | Running |

## Storage Layout

| Storage ID | Type | Path | Content |
|------------|------|------|---------|
| local | dir | /var/lib/vz | ISO, backup, templates |
| local-lvm | LVM-thin | pve/data | VM images, rootdir |
| bi-archive | dir | /mnt/pve/bi-archive | Blue Iris images |
| hdd-pool | ZFS | /hdd-pool | VM disks (frigate) |

## Network

- **vmbr0:** 192.168.1.174/24 (LAN bridge)
- **tailscale0:** 100.65.215.41/32
- **Docker bridges:** 172.17.0.1/16, 172.18.0.1/16

## Notes

- Single-node Proxmox cluster (no clustering)
- Frigate uses Coral TPU for object detection (7 cameras, 10.48ms inference)
- Blue Iris VM is the main CPU consumer (~490% on 10 vCPUs)
- ZFS hdd-pool rebuilt 2026-05-07 — detached dead mirror, single vdev ONLINE
