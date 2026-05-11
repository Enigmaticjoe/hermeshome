# Pi-hole DNS Configuration

## Primary Pi-hole
- **Location:** Node B (192.168.1.222)
- **Ports:** :53 (DNS), :8081 (Web UI)
- **Image:** pihole/pihole:latest
- **Password:** 12121212
- **Upstream DNS:** Cloudflare 1.1.1.1 / 1.0.0.1
- **Time zone:** America/Chicago

## DNS Resolution
All internal and external services resolve through Pi-hole.
Wildcard *.happystrugglebus.us routes through Cloudflare.

## Chimera Neural Fabric DNS
Custom DNS entries managed via Pi-hole API.
See: https://git.happystrugglebus.us/jbauer/rabbit-hole
