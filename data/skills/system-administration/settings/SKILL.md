---
name: settings
description: Manage app settings, preferences, endpoints, and integrations
version: 1.0.0
category: system-administration
tags: [settings, preferences, endpoints, mcp, webhooks, tokens]
status: published
confidence: 0.80
source: user
owner: admin
created: "2026-06-13T02:35:00Z"
---

## When to Use

Use this skill when the user wants to change app settings, add/remove AI model endpoints, configure MCP servers, manage webhooks, or generate API tokens.

Key phrases: "change a setting", "add an endpoint", "remove an endpoint", "add an MCP server", "manage webhooks", "generate an API token", "change my preferences".

## Prerequisites

This skill requires these native tools:
- `manage_settings` — Change app settings and tool toggles
- `manage_endpoints` — Add, remove, and configure AI model endpoints
- `manage_mcp` — Manage MCP tool servers (add, remove, configure)
- `manage_webhooks` — Configure outgoing webhooks
- `manage_tokens` — Generate and revoke API tokens

## Procedure

### Step 1: Identify what the user wants to change

Listen for keywords to determine which tool to use:

| User mentions | Tool |
|--------------|------|
| "Setting", "preference", "tool toggle", "enable/disable X" | `manage_settings` |
| "Endpoint", "model provider", "API URL", "add model" | `manage_endpoints` |
| "MCP server", "external tool", "connect X tool" | `manage_mcp` |
| "Webhook", "notify X when Y" | `manage_webhooks` |
| "API key", "token", "generate key" | `manage_tokens` |

### Step 2: Choose the right action

**Settings (manage_settings):**
- List current settings / preferences
- Get individual setting value
- Set/change a setting
- Disable/enable tools globally (`disable_tool` / `enable_tool`)
- Tool aliases: shell, search, browser, documents, memory, skills, images, tasks, notes, calendar, email — or raw tool names like `bash` or `web_search`

**Endpoints (manage_endpoints):**
- List configured endpoints — shows registered AI model endpoints
- Add a new endpoint (API URL, key, model list)
- Update an existing endpoint
- Remove/delete an endpoint
- Test an endpoint connection

**MCP (manage_mcp):**
- List registered MCP servers
- Add an MCP server (command, args, env vars)
- Update an existing MCP server config
- Remove an MCP server
- Toggle MCP server enabled/disabled

**Webhooks (manage_webhooks):**
- List configured webhooks
- Add a webhook (URL, events to trigger on, format)
- Update webhook config
- Delete a webhook
- Test a webhook

**Tokens (manage_tokens):**
- List existing tokens
- Generate a new API token
- Revoke an existing token

### Step 3: Confirm changes

After making any change, confirm what was done:
- "Updated the temperature setting to 0.7"
- "Added [OpenRouter endpoint](#endpoint-<id>)"
- "Generated a new API token — share it with the user ONCE, then it's gone forever"

## Pitfalls

1. **Prefer named tools over app_api:** These tools are purpose-built for their tasks. Use them instead of `app_api` which has restricted permissions.
2. **Token security:** When generating a token, show it to the user AT THAT MOMENT. It won't be shown again.
3. **Endpoints need testing:** After adding/modifying an endpoint, test it before declaring success.
4. **MCP server env vars:** When adding an MCP server, check if it needs environment variables (API keys, URLs, etc.) and prompt the user if they're not provided.
5. **Destructive actions:** Before deleting endpoints, MCP servers, or revoking tokens, confirm with the user — especially if they might be actively in use.

## Verification

- Settings changes are reflected in the app
- New endpoints appear in the model dropdown
- MCP servers connect and show tools
- Webhooks fire on their configured events
- Generated tokens authenticate API requests