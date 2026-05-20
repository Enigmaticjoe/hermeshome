# HERMES_NEXT_ACTIONS.md — v2 (Local-First Migration Complete)

> Updated: 2026-05-20
> Status: LiteLLM fixed, Hermes default changed, token economy enabled.

---

## P0 — DO NOW

### 1. Start vLLM on Node A
**Why:** RX 7900 XT (20GB) is completely idle. Qwen3-14B-AWQ would add a powerful free local tier.
**What:**
```bash
cd ~/git/shite
docker compose -f compose/dev/00-ai-stack.yml up -d
# Verify: curl http://192.168.1.11:8000/v1/models
# Then uncomment brain-heavy in LiteLLM config at /mnt/user/appdata/shite/gateway/litellm-config.yaml
# Add to fallback chain: hermes-code → brain-heavy → hermes-deepseek
```

### 2. Fix Qwen3 Reasoning Field
**Why:** qwen3:4b (2.5GB), qwen3:8b (5.2GB), qwen3:14b (9.3GB) all return empty content via LiteLLM v1.85.0 because the `reasoning` field is stripped. These are the fastest models on Node B.
**What:** Either upgrade LiteLLM to a version that passes `reasoning` through, or wait for v1.86.0+ which may fix this.

---

## P1 — DO TODAY

### 3. Verify Local-First is Working
**Check:** The Hermes config at `~/.hermes/config.yaml` now defaults to `hermes-auto` via `litellm`. Run a few queries to confirm:
```bash
hermes "hello"
hermes "what is 2+2"
# Both should respond in <2s and use local models ($0 cost)
```

### 4. Update Docs
- Node S (StephAI, 192.168.1.132) missing from README/TOPOLOGY/CHIMERA_REPORT
- Node A GPU swapped (Kali vs brain, RTX 4070 vs RX 7900 XT)
- Container counts outdated (76 → 79)
- See NORMALIZATION_REPORT.md for all 15 contradictions

---

## P2 — DO THIS WEEK

### 5. Test DeepSeek Fallback
**Want to confirm:** When local models fail or context is too large, LiteLLM correctly falls back to DeepSeek.
**Test:** `hermes -m hermes-deepseek "write a 5000-word essay about AI"` — should use DeepSeek API.

### 6. Set Up Monitoring
- Add LiteLLM health check to Uptime Kuma (:3010)
- Set up Langfuse dashboard for DeepSeek cost tracking
- Configure Dozzle (:8888) for LiteLLM log watching

---

## P3 — NICE TO HAVE

### 7. Node C Models via LiteLLM
qwen2.5:7b on Node C (Arc A770) is registered as `arc-reason` but not tested through LiteLLM fallback.

### 8. Start vLLM After UNITY
Once vLLM is running, add it to the fallback chain for a proper 4-tier local stack.

---

## Quick Reference — Current State

| Service | Status | URL |
|---------|--------|-----|
| LiteLLM Gateway | ✅ v1.85.0, 17 models | http://192.168.1.222:4000 |
| Ollama Node B | ✅ 9 models, RTX 4070 | http://192.168.1.222:11434 |
| Ollama Node C | ✅ 5 models, Arc A770 | http://100.100.88.37:11434 |
| vLLM Node A | ❌ Not running | http://192.168.1.11:8000 |
| Hermes CLI | ✅ Default hermes-auto | LiteLLM gateway |
| DeepSeek | ✅ Final fallback | Paid API (~$0.10/wk target) |
