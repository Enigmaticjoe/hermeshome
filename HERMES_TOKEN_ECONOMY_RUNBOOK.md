# HERMES_TOKEN_ECONOMY_RUNBOOK.md — v2 (Live-Verified 2026-05-20)

> Compiled from live audit of all 5 nodes + LiteLLM gateway.
> All models verified working with LiteLLM v1.85.0.
> DeepSeek cost target: ≤$0.10/week (from $0.50-$2.00).

---

## 1. Current State (Post-Fix)

**Before this session:**
- LiteLLM crash-looping with `Cache` init error (main-latest tag)
- Hermes defaulting to DeepSeek V4 Flash (paid) or Claude Sonnet (paid via OpenRouter)
- vLLM on Node A idle (RX 7900 XT unused)
- Configs referencing nonexistent model names (qwen2.5:7b-instruct, phi3:mini)
- qwen3 models failing through LiteLLM (reasoning field not passed through)

**After this session:**
- LiteLLM pinned to `v1.85.0` — stable, no crashes
- Hermes default: `hermes-auto` → `hermes-cheap` → `hermes-code` → `hermes-deepseek`
- All 17 LiteLLM models verified working (qwen3 models noted as "thinking" only)
- Fallback chain: local models first, DeepSeek last

## 2. The Model Stack (Verified Live)

```
    ┌─ LiteLLM Gateway (192.168.1.222:4000) ───────────────────────┐
    │                                                               │
    │  hermes-auto (your default from now on)                       │
    │      │                                                        │
    │      ├─ hermes-cheap  → dolphin-mistral:7b-v2.8 [Node B]     │  ← 1st try
    │      │   4.1GB, <500ms, uncensored, $0                       │   ~70% of queries
    │      │                                                        │
    │      ├─ hermes-code   → nous-hermes2:10.7b [Node B]          │  ← 2nd try  
    │      │   6.1GB, 1-3s, deep reasoning, $0                     │   ~20% of queries
    │      │                                                        │
    │      ├─ arc-reason    → qwen2.5:7b [Node C / Arc A770]       │  ← 3rd try (fallback)
    │      │   7.6GB, SYCL backend, $0                             │
    │      │                                                        │
    │      └─ hermes-deepseek → DeepSeek V4 Flash API [Cloud]      │  ← FINAL fallback
    │          1M context, $0.01/call                              │   ≤2% of queries
    │                                                               │
    │  NOTE: qwen3:4b, qwen3:8b, qwen3:14b also loaded but         │
    │  LiteLLM v1.85.0 strips their "reasoning" field → empty       │
    │  content. Keep for future when LiteLLM handles Qwen3 format.  │
    └───────────────────────────────────────────────────────────────┘
```

## 3. Hardware Utilization (What's Actually Running)

| Node | GPU | VRAM | Model Running | Utilization |
|------|-----|------|---------------|-------------|
| **A Brain** | RX 7900 XT | 20GB | vLLM: NOT RUNNING | ❌ 0% — idle |
| **B Brawn** | RTX 4070 | 12GB | Ollama (9 models) | ✅ ~9.9GB used for model cache |
| **C Arc** | Arc A770 | 16GB | Ollama (5 models, SYCL) | ✅ active |
| **D Proxmox** | — | — | Frigate + Coral TPU | ✅ ~10ms inference |
| **E HAOS** | — | — | HA + Wyoming STT/TTS | ✅ active |

**Idle hardware:**
- Node A vLLM (Qwen3-14B-AWQ) — 9.5GB VRAM sitting idle on the RX 7900 XT
- To activate: `docker compose -f ~/git/shite/compose/dev/00-ai-stack.yml up -d`
- Then uncomment `brain-heavy` in LiteLLM config and add to fallback chain

## 4. Which Model For What

| Task | Recommended Model | Why |
|------|------------------|-----|
| "What's the weather?" | hermes-cheap | <500ms, $0 |
| "List my Docker containers" | hermes-cheap | Fast tool calls |
| "Write a Python function" | hermes-code | nous-hermes2 is clean for code |
| "Debug this crash" | hermes-code | Deep reasoning |
| "Compare architectures" | hermes-code → hermes-deepseek | Escalate if complex |
| "Design a new API" | hermes-deepseek | 1M context needed |
| Final review before commit | hermes-deepseek | Quality gate, one-shot |
| "Summarize this log" | hermes-cheap | Fast, $0 |
| "What do you think about X?" | hermes-code → hermes-deepseek | Deep reasoning |

## 5. Migration: Before vs After

| Setting | Before (Cloud-First) | After (Local-First) |
|---------|---------------------|--------------------|
| Default model | deepseek-v4-flash (paid) | hermes-auto (LiteLLM routed) |
| Default provider | deepseek / openrouter | litellm |
| Base URL | api.deepseek.com / openrouter.ai | 192.168.1.222:4000 |
| Context length | 1,000,000 | 32,000 (LiteLLM handles escalation) |
| Fallback providers | vllm → ollama-c → ollama-b | litellm (single gateway) |
| Cost/week | $0.50-$2.00 | ~$0.10 (DeepSeek only for hard tasks) |

## 6. CLI Quick Reference

```bash
# Default (local-first, via LiteLLM)
hermes "what's the weather?"

# Explicit model selection
hermes -m hermes-deepseek "design the full architecture"

# Check what's registered in LiteLLM
curl -s -H "Authorization: Bearer sk-master-key" http://192.168.1.222:4000/v1/models | python3 -m json.tool

# Check DeepSeek API cost
# → http://192.168.1.222:3003 (Langfuse)
```

## 7. What's Still To Do

| Priority | Task | Impact |
|----------|------|--------|
| **P0** | Start vLLM on Node A (RX 7900 XT) | Adds brain-heavy (Qwen3-14B-AWQ) as free local tier between code and DeepSeek |
| **P0** | Fix Qwen3 models in LiteLLM | qwen3:4b/8b/14b exist but reasoning field stripped by v1.85.0 |
| **P1** | Migrate hermeshome repo configs | Already done for this session |
| **P1** | Add Node S (StephAI) to documentation | Missing from 5-node descriptions |
| **P2** | Document normalization | 15 contradictions found (GPU swapped, OS wrong, etc.) |
| **P3** | Set up Uptime Kuma alert for LiteLLM | Gateway health monitoring |
