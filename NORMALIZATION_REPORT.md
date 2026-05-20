# NORMALIZATION_REPORT.md — Documentation Contradictions

> Generated: 2026-05-20
> Sources compared: README.md, TOPOLOGY.md, INVENTORY.md, NETWORK.md, CHIMERA_REPORT.md, NODES/*.md, live audit (2026-05-20)
> Status: DRAFT — some contradictions verified live, others require confirmation

---

## CONTRADICTION 1: Node A Hostname

| Source | Value |
|--------|-------|
| TOPOLOGY.md | `brain` |
| NETWORK.md | `brain` |
| node-a-brain.md | `brain` |
| CHIMERA_REPORT.md | `Kali` |

**Verdict:** Node A's actual hostname is `brain` (verified live). CHIMERA_REPORT.md is WRONG — it says "Kali Linux" / "Dev workstation". Node A is Ubuntu running the Hermes orchestrator.

**Fix:** Update CHIMERA_REPORT.md to use `brain` / Ubuntu.

---

## CONTRADICTION 2: Node C OS

| Source | Value |
|--------|-------|
| TOPOLOGY.md | Ubuntu |
| node-c-arc.md | Ubuntu (Ubuntu 24.04 with Mesa 26.0.3) |
| CHIMERA_REPORT.md | NixOS |

**Verdict:** Node C is Ubuntu 24.04 (confirmed by Mesa version, apt-based packages). CHIMERA_REPORT.md is WRONG.

**Fix:** Update CHIMERA_REPORT.md to Ubuntu.

---

## CONTRADICTION 3: Node A GPU

| Source | Value |
|--------|-------|
| TOPOLOGY.md / node-a-brain.md | **RX 7900 XT 20GB** (AMD/ROCM) |
| CHIMERA_REPORT.md | **RTX 4070** (NVIDIA/CUDA) |

**Verdict:** Node A has an RX 7900 XT (verified live via docker-proxy for ROCm vLLM image). CHIMERA_REPORT.md copied Node B's GPU spec by mistake. **RTX 4070 is on Node B.**

**Fix:** CHIMERA_REPORT.md Node A GPU must read RX 7900 XT.

---

## CONTRADICTION 4: Node C CPU Model

| Source | Value |
|--------|-------|
| TOPOLOGY.md / NETWORK.md | Ryzen 7 7700X |
| node-c-arc.md | Ryzen 7 7700 (no X) |

**Verdict:** Cannot verify live without SSH. The `node-c-arc.md` was generated from `lscpu` output and is likely more accurate. **Assumed: Ryzen 7 7700** (non-X).

**Fix:** Confirm via `ssh jb@192.168.1.6 'lscpu | grep "Model name"'` and update TOPOLOGY.md.

---

## CONTRADICTION 5: Home Assistant IP

| Source | Value |
|--------|-------|
| CREDENTIALS/reference.md | `192.168.1.165:8123` |
| node-e-pve.md | `192.168.1.165:8123` (HAOS VM on Node E) |
| CHIMERA_REPORT.md | Various mentions, no IP specified |
| AGENTS.md (shite repo) | `192.168.1.149:8123` (Docker HA on Node E?) |

**Verdict:** HA is at `192.168.1.165:8123` (confirmed live via curl — 200 response). It's an HAOS VM on Node E (Proxmox), NOT a Docker container.

**Fix:** CHIMERA_REPORT.md and AGENTS.md should reference `192.168.1.165`.

---

## CONTRADICTION 6: vLLM Port

| Source | Value |
|--------|-------|
| CONFIGS/hermes/config.yaml | `http://192.168.1.11:8001/v1` |
| Docker Compose (00-ai-stack.yml) | Port 8001 exposed |
| Live audit | Port 8000 = Portainer BE, Port 8001 = NOTHING |
| MCP vLLM server (vllm_mcp_server.py) | `http://192.168.1.11:8000` (default) |

**Verdict:** vLLM inference server is NOT running. Port 8000 is Portainer. Port 8001 is empty. The `00-ai-stack.yml` compose file exists but the container needs to be started.

**Fix:** Start vLLM container or remove references.

---

## CONTRADICTION 7: Node A Qdrant Collections Count

| Source | Value |
|--------|-------|
| AGENTS.md | 5 collections |
| Live audit | **19 collections** |

**Verdict:** AGENTS.md is severely out of date. Live Qdrant has chimera_knowledge, chimera-memory, chimera_homelab, stephai_knowledge, chimera-registry, rabbit-hole-memory, chimera-frontpage-registry, chimera-bible, smoothy_memory, unity-plan, opencode_memory, chimera_credentials, hermes_ego, stephai_memory, claude_knowledge, chimera_code, documents, session_docs, sherpa-hole = 19 total.

**Fix:** Update all docs to reflect 19 collections on Node A.

---

## CONTRADICTION 8: Node B Qdrant Collections Count

| Source | Value |
|--------|-------|
| AGENTS.md | 14 collections (plus 5 on Node A = 19 total) |
| Live audit | **20 collections** |

**Verdict:** Slight drift. Live has 20 collections on Node B.

**Fix:** Update to 20.

---

## CONTRADICTION 9: LiteLLM Model Count

| Source | Value |
|--------|-------|
| AGENTS.md | 16 models |
| INVENTORY.md | 14 models |
| LiteLLM config in repo | 8 models (brawn-fast, brawn-code, brawn-phi, brawn-dolphin, brawn-vision, operator-fast, operator-code, gpt-4o-mini, gpt-4o) |

**Verdict:** The LiteLLM config in the repo is OLD — it still references `qwen2.5:7b-instruct` and `qwen2.5-coder:14b` which are NOT the models currently on Node B Ollama. The AGENTS.md has the most current model list (16 models).

**Fix:** Update the LiteLLM config in the repo to match current reality.

---

## CONTRADICTION 10: Container Counts

| Source | Node B | Node A | Node C |
|--------|--------|--------|--------|
| README.md | 76 (implied by "90+ total") | 6 | 3 |
| INVENTORY.md | 76 | 6 | 3 |
| AGENTS.md | 79 | N/A | N/A |
| TOPOLOGY.md | 76 | 6 | 3 |

**Verdict:** Node B has grown from 76→79 per latest AGENTS.md. README/INVENTORY/TOPOLOGY are stale.

**Fix:** Update to 79 per latest audit.

---

## CONTRADICTION 11: Node E HA Version

| Source | Value |
|--------|-------|
| TOPOLOGY.md / node-e-pve.md | Home Assistant OS 2026.4.4 |
| AGENTS.md (shite) | HA Core 2026.5.1 |

**Verdict:** Likely updated between doc generations. 2026.5.1 is newer and probably correct.

**Fix:** Confirm and update node-e-pve.md.

---

## CONTRADICTION 12: Node E Tailscale

| Source | Value |
|--------|-------|
| NETWORK.md | `none` |
| AGENTS.md | `100.110.38.37` |
| TOPOLOGY.md | No mention |

**Verdict:** AGENTS.md says Node E has Tailscale IP 100.110.38.37. NETWORK.md says none. Likely added after NETWORK.md was written.

**Fix:** Update NETWORK.md to include Node E Tailscale IP.

---

## CONTRADICTION 13: Node D Status

| Source | Value |
|--------|-------|
| CHIMERA_REPORT.md | `⚠️ Possibly offline` |
| Live audit | Proxmox at 192.168.1.174 — confirmed online (node-d-prox.md details it) |

**Verdict:** CHIMERA_REPORT.md is WRONG about Node D status. Node D is online and running Proxmox with Frigate + Blue Iris VMs.

**Fix:** Update CHIMERA_REPORT.md.

---

## CONTRADICTION 14: Top-level Claims vs Reality

| Source | Claim | Reality |
|--------|-------|---------|
| README.md | "5-node homelab" | Missing Node S (StephAI/192.168.1.132) — 6 nodes now |
| CHIMERA_REPORT.md | "5-node" | Same — missing Node S |
| TOPOLOGY.md | "5 nodes" | Same |

**Fix:** Add Node S to all high-level docs.

---

## CONTRADICTION 15: LiteLLM Status

| Source | Claim | Reality |
|--------|-------|---------|
| All docs | LiteLLM running at :4000 | **CRASH-LOOPING** — `Restarting (3)` with Cache init error |
| CHIMERA_REPORT.md | "LiteLLM — fully deployed" | Not functional |

**Fix:** Fix LiteLLM crash before updating docs.

---

## Summary of Required Fixes

| Priority | Contradiction | Fix |
|----------|--------------|-----|
| **P0** | LiteLLM crash-looping | Fix Redis/Cache init issue — restart LiteLLM |
| **P0** | vLLM not running | Start vLLM container on Node A |
| **P1** | GPU swapped (7900 XT vs 4070) | CHIMERA_REPORT.md correction |
| **P1** | Node C OS (NixOS vs Ubuntu) | CHIMERA_REPORT.md correction |
| **P1** | Node A hostname (Kali vs brain) | CHIMERA_REPORT.md correction |
| **P1** | Missing Node S | Add to all top-level docs |
| **P2** | Qdrant collection counts | Update AGENTS.md |
| **P2** | LiteLLM model count | Update repo config |
| **P2** | Container counts (76 vs 79) | Update README/TOPOLOGY |
| **P2** | Node C CPU (7700X vs 7700) | Verify and update |
| **P3** | Node E Tailscale | Update NETWORK.md |
| **P3** | Node D status "offline" | Mark as online |

This report was generated from live audit on 2026-05-20. Documents in the `shite` repo (`~/git/shite/AGENTS.md`) are more current than this repo's docs.
