# Credential Reference
> Placeholder values — actual secrets are in ~/git/shite/secrets/chimera-secrets.yaml

## SSH Access
| Node | User | Password | Method |
|------|------|----------|--------|
| A (brain) | jb | 1212 | Direct SSH |
| B (brawn) | root | 12121212 | Via Tailscale (100.79.79.25) |
| C (nodec) | jb | 1212 | Via Tailscale (100.100.88.37) or LAN |
| D (prox) | root | 12121212 | Direct LAN |
| E (pve-node-e) | root | 12121212 | Direct LAN |

## Web Services
| Service | URL | Username | Password |
|---------|-----|----------|----------|
| Media Portal | https://media.happystrugglebus.us | josh | 12121212 |
| Portainer | https://portainer.happystrugglebus.us | admin | 121212121212 |
| Forgejo | https://git.happystrugglebus.us | jbauer | 12121212 |
| Pi-hole | https://pihole.happystrugglebus.us:8081 | admin | 12121212 |
| Home Assistant | http://192.168.1.165:8123 | jb | 12alora34 |
| Hermes WebUI | https://hermes.happystrugglebus.us | admin | 12alora34 |

## API Keys
| Service | Key/Location |
|---------|-------------|
| DeepSeek API | ~/.env.chimera, ~/.hermes/config.yaml |
| LiteLLM Master | sk-master-key |
| Plex Token | AQzj8-4b56cZddtn9Q6q |
| Prowlarr API | fc508a712b5b4d4e96884faf15e886c3 |
| Authelia Session Secret | 65fca9db4f0243a95453927839e20239 |
| Home Assistant Token | ~/.env.chimera (10-year expiry) |
| Tailscale Auth Key | ~/.env.chimera (expires Aug 2026) |
| Cloudflare API Token | ~/.env.chimera |
| Forgejo | admin jbauer / 12121212 |
