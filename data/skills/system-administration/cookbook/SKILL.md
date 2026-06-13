---
name: cookbook
description: Manage AI model serving — launch, stop, monitor, and download models
version: 1.0.0
category: system-administration
tags: [cookbook, models, serving, vllm, llama.cpp, ollama]
status: published
confidence: 0.85
source: user
owner: admin
created: "2026-06-13T02:20:00Z"
---

## When to Use

Use this skill when the user asks about the Cookbook — serving models, downloading, checking what's running, stopping servers. "Cookbook" is the LLM-serving subsystem, NOT a recipe app.

Key phrases: "what's running", "serve this model", "download that model", "kill the server", "show downloads", "what models do I have", "start SD 3.5 on gpu-box", "adopt that orphaned server".

## Prerequisites

This skill requires these native tools:
- `list_served_models` — Show what's currently running (ALWAYS available — call it)
- `list_downloads` — Show in-progress downloads
- `list_cached_models` — Show models on disk
- `list_serve_presets` — Show saved launch templates
- `list_cookbook_servers` — Show configured remote hosts
- `serve_preset` — Launch a model from a saved template
- `serve_model` — Launch a model with custom command
- `stop_served_model` — Stop a running server
- `download_model` — Download a HuggingFace model
- `cancel_download` — Cancel an in-progress download
- `search_hf_models` — Search HuggingFace for models
- `adopt_served_model` — Register an orphaned server in the cookbook

## Procedure

### Step 1: Check BEFORE acting

When the user asks anything cookbook-related, start with the relevant list tool:

| User says | First call |
|-----------|-----------|
| "What's running" / "is anything up" | `list_served_models` |
| "What's downloading" | `list_downloads` |
| "What models do I have" | `list_cached_models` |
| "Serve X" / "run X" | `list_serve_presets` first, THEN `serve_preset` or `serve_model` |
| "On gpu-box" / "that server" | `list_cookbook_servers` to find available hosts |

Do NOT use `ps aux`, `curl localhost:8000`, or `which vllm` to check — these tools are the source of truth.

### Step 2: Choose the right action

**Serving a model:**
1. First check presets: `list_serve_presets` — if a matching preset exists, use `serve_preset`
2. If no preset: `serve_model` with `repo_id`, `cmd` (the full launch command), and optional `host`
3. ALWAYS go through the cookbook — never use `bash` to start a tmux session manually
4. After launching, verify with `list_served_models`

**Stopping:**
- `stop_served_model` with the `session_id` from `list_served_models`

**Downloading:**
- `download_model` with `repo_id` (e.g. "unsloth/DeepSeek-R1-GGUF")
- Check progress with `list_downloads`
- Cancel with `cancel_download`

**Adopting orphaned servers:**
- If you find a running server the cookbook doesn't know about, use `adopt_served_model` with `host`, `tmux_session`, `model`, `port`
- This registers it AND adds it as a chat endpoint

### Step 3: Host awareness

- If the user names a host ("on gpu-box", "on the GPU server"), pass `host=` to the tool
- If they don't name one, the tool defaults to the currently-selected server
- When ambiguous, call `list_cookbook_servers` and ask
- Download to localhost only when the user explicitly says "locally" / "on this machine"

## Pitfalls

1. **NEVER use bash/ssh/tmux:** The biggest anti-pattern. `serve_model` creates the tmux session AND registers it in cookbook state. Bash-launched servers are invisible to the UI and can't be stopped via the cookbook.
2. **Presets first:** Always check `list_serve_presets` before creating a custom launch. The user may have saved working templates.
3. **Verify after launch:** Always call `list_served_models` after serving to confirm it's running. If it gives a diagnosis and adjusted command, retry with that command instead of asking the user to debug.
4. **NO app_api for cookbook:** POSTing to `/api/cookbook/state` via `app_api` overwrites the entire state file. Use the named tools.
5. **Image models:** For "serve SDXL inpainting" / "run an image model", use `serve_model` with the diffusers command: `python3 scripts/diffusion_server.py --model <repo> --port 8100`. Do NOT invent module names.
6. **list_served_models is ALWAYS available:** Even if you don't remember seeing it in your tool list, just call it. It's there.

## Verification

- `list_served_models` shows launched servers after a serve attempt
- `list_downloads` shows progress bars for in-progress downloads
- Stopped servers disappear from the served list
- Adopted servers appear in the served list AND as chat endpoints