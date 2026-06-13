---
name: sessions
description: Manage chat sessions — rename, archive, delete, fork, switch, and list chats
version: 1.0.0
category: system-management
tags: [sessions, chats, history, conversations]
status: published
confidence: 0.85
source: user
owner: admin
created: "2026-06-13T02:15:00Z"
---

## When to Use

Use this skill when the user asks about managing their chat sessions — "rename this chat", "show my chats", "find that conversation about X", "delete old chats", "archive this", "switch to the coding chat", "fork this into a new chat".

## Prerequisites

This skill requires these native tools:
- `list_sessions` — List all chat sessions, newest first. Preserves clickable links.
- `manage_session` — Rename, archive, delete, fork, switch sessions
- `search_chats` — Search past chat transcripts

## Procedure

### Step 1: List or search first

When the user asks about a past conversation:
- "Find that chat about X" → `search_chats` with the topic/query
- "Show my chats" → `list_sessions` to see all sessions
- "What chats do I have" → `list_sessions`

Both return sessions with IDs — preserve the clickable links when presenting them to the user.

### Step 2: Choose the right action

**Renaming:**
- "Rename this chat to X" → `manage_session` with `action: "rename"`, `id: <session_id>`, `name: "New Name"`

**Archiving:**
- "Archive this chat / hide it" → `manage_session` with `action: "archive"`, `id: <session_id>`
- Archived chats are hidden but not deleted

**Deleting:**
- "Delete this chat" → `manage_session` with `action: "delete"`, `id: <session_id>`
- "Delete all old chats" — list first, then delete each

**Forking:**
- "Fork / branch / copy this chat" → `manage_session` with `action: "fork"`, `id: <session_id>`, and optionally a new name

**Switching:**
- "Switch to the coding chat" → `manage_session` with `action: "switch"`, `id: <session_id>`

**Creating a new chat:**
- "Start a new chat" / "new conversation" → `create_session` with optional `name` and/or `character_name`

### Step 3: Use clickable links

- Render chat links as: `[Chat title](#session-<id>)`
- In lists, tables, or prose — always preserve the clickable format
- After creating: "Created [New Chat](#session-abc123) — click to switch"
- After searching: present results with clickable links

## Pitfalls

1. **Don't shell out:** Chat data lives in this app's database. Do NOT try to find sqlite files, curl localhost, or grep for routers. `list_sessions` is the source of truth.
2. **Preserve links:** When the user asks "what chats do I have", do NOT rewrite the list as a plain table. Use the clickable link format from `list_sessions` output.
3. **Search first for specific chats:** If the user wants a chat about a specific topic, `search_chats` is much more targeted than `list_sessions`.
4. **Delete vs archive:** Archiving hides but doesn't destroy. Deleting is permanent. Ask if unsure.
5. **You are INSIDE Odysseus:** There is no OpenWebUI, ChatGPT, or external chat backend. All sessions are in THIS app.

## Verification

- `list_sessions` returns sessions with IDs and names
- `search_chats` returns relevant chat matches
- Renamed sessions show the new name in subsequent lists
- Archived sessions disappear from normal list results
- Deleted sessions are truly gone