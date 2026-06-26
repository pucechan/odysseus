---
name: api-call
description: Call configured external service integrations through api_call instead of shell, curl, or app_api.
version: 1.0.0
category: integrations
tags: [integrations, api_call, home-assistant, miniflux, gitea, linkding, jellyfin]
status: published
confidence: 0.85
source: user
owner: admin
created: "2026-06-26T21:05:00Z"
---

## When to Use

Use this skill when the user asks to query or control a configured external service integration, such as Home Assistant, Miniflux, Gitea, Linkding, Jellyfin, or another registered API service.

Typical requests:

- "Use Home Assistant to check the living room lights."
- "Call the Home Assistant states endpoint."
- "Ask Miniflux for unread feeds."
- "Create a Linkding bookmark."
- "Check my Gitea issues."
- "Use the api_call tool to GET /api/states."

Do **not** use this skill for:

- Odysseus internal UI/API actions when a named tool exists.
- Shell/curl/python HTTP calls to a configured integration.
- Managing the integration configuration itself — use settings/integration tools for that.

## Prerequisites

This skill requires the native tool:

- `api_call` — call a configured integration by name, HTTP method, path, and optional JSON body.

## Procedure

### Step 1: Identify the integration and API action

Extract:

- integration/service name, such as `Home Assistant`, `Miniflux`, `Gitea`, `Linkding`, or `Jellyfin`
- HTTP method: usually `GET`, `POST`, `PUT`, `PATCH`, or `DELETE`
- path, such as `/api/states`, `/api/services/light/turn_on`, `/api/entries`, `/repos/...`
- optional JSON body

If the user did not specify a method, default to `GET` for read/list/status requests and `POST` for actions that change state.

### Step 2: Use api_call, not shell

Call `api_call` with the integration name, method, path, and body. Do not run `curl`, Python requests, shell commands, or `app_api` to reach a configured integration.

Example intent mapping:

- "Home Assistant GET /api/states" → `api_call` with integration `Home Assistant`, method `GET`, path `/api/states`
- "Turn on the living room lamp" → likely Home Assistant `POST` to a service path with an entity/body, if enough information is known
- "List unread Miniflux entries" → Miniflux integration, read/list endpoint

### Step 3: Handle missing details

If a state-changing call is ambiguous or could affect the wrong device/repo/feed, ask one concise clarification question.

Examples:

- "Which light/entity should I turn on?"
- "Which repository should I query?"

For harmless read-only requests, make the best call available from the user's path/service name.

### Step 4: Summarize the result

After the tool returns, summarize the important result. Do not dump huge JSON unless the user asked for raw output.

If the call fails, report the status/error and suggest the likely fix, such as checking the integration name, path, method, or configured credentials.

## Pitfalls

- **Do not use curl/shell for configured integrations.** The integration already has stored credentials and base URL.
- **Do not use app_api for external services.** `app_api` is for internal Odysseus API actions only when no named tool exists.
- **Do not invent integration names.** Use the name the user gives; if unsure, ask or list/configure integrations if that tool is available.
- **Be careful with state-changing requests.** If the target is ambiguous, clarify before POST/PATCH/DELETE.
- **Keep raw JSON concise.** Summarize by default.

## Verification

- The response came from `api_call`, not shell/curl.
- The method/path match the user's request.
- State-changing calls target the intended service/entity.
- Errors are reported from the tool output rather than hidden.
