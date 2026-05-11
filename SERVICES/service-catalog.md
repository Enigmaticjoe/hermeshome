# Service Catalog — Caddy Subdomain Routing

All services accessible at `*.happystrugglebus.us` through:
Cloudflare Tunnel → Caddy (:80) → Authelia forward_auth → backend

## Routing Table

| Subdomain | Backend (Node B) | Backend Port | Auth |
|-----------|-----------------|-------------|------|
| auth | Authelia | :9091 | Bypass |
| media | Media Portal | :4343 | SSO |
| plex | Plex | :32400 | SSO |
| jellyfin | Jellyfin | :8096 | SSO |
| stremio | Stremio | :11470 | SSO |
| overseerr | Overseerr | :5055 | SSO |
| sonarr | Sonarr | :8989 | SSO |
| radarr | Radarr | :7878 | SSO |
| lidarr | Lidarr | :8686 | SSO |
| prowlarr | Prowlarr | :9696 | SSO |
| bazarr | Bazarr | :6767 | SSO |
| whisparr | Whisparr | :6969 | SSO |
| readarr | Readarr | :8787 | SSO |
| sabnzbd | SABnzbd | :8080 | SSO |
| qbittorrent | qBittorrent | :8282 | SSO |
| tautulli | Tautulli | :8181 | SSO |
| portainer | Portainer | :9443 | SSO |
| homepage | Homepage | :3002 | SSO |
| hermes | Hermes WebUI | :8777 | SSO |
| stash | Stash | :9998 | None |
| riven | Riven | :6191 | SSO |
| zurg | Zurg | :6192 | SSO |
| vault | Vaultwarden | :8200 | SSO |
| forgejo | Forgejo | :3000 | SSO |
| openwebui | Open WebUI | :3001 | SSO |
| n8n | n8n | :5678 | SSO |
| audio | Audiobookshelf | :13378 | SSO |
| chimera | Node A (:8888) | 192.168.1.11:8888 | SSO |
| downloads | File server | /mnt/user/media/downloads | None |
| debug | Debug endpoint | N/A | None |

## Notes
- All SSO services require authentication via Authelia (one_factor)
- stash, downloads, and debug bypass Authelia
- chimera routes to Node A (192.168.1.11) instead of Node B localhost
- Caddy listens on :80 only; TLS is handled by Cloudflare at edge
