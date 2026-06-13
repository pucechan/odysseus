---
name: ui-control
description: Control the UI — open panels, toggle tools, set themes, and email drafts
version: 1.0.0
category: system-management
tags: [ui, panels, themes, toggles, controls]
status: published
confidence: 0.85
source: user
owner: admin
created: "2026-06-13T02:30:00Z"
---

## When to Use

Use this skill when the user wants to interact with the Odysseus UI — opening panels, toggling tools on/off, changing themes, creating custom themes, or opening email reply drafts. Think of this as the remote control for the app interface.

Key phrases: "open my memories", "show me my skills", "turn off web search", "change the theme to dark", "make a retro wave theme", "open a reply to that email", "open the gallery".

## Prerequisites

This skill requires one native tool:
- `ui_control` — Control the UI with actions: `open_panel`, `toggle`, `open_email_reply`, `set_theme`, `create_theme`, `set_mode`, `switch_model`

## Procedure

### Step 1: Understand the action types

| User wants | Action | Example |
|-----------|--------|---------|
| Open a panel | `open_panel <name>` | `open_panel skills` |
| Toggle a tool | `toggle <name> <on\|off>` | `toggle bash on` |
| Change theme | `set_theme <name>` | `set_theme midnight` |
| Create custom theme | `create_theme <name> <colors>` | `create_theme "Sunset" {bg: "#...", ...}` |
| Open email reply | `open_email_reply <uid> <folder> reply` | `open_email_reply 90186 INBOX reply` |
| Switch chat mode | `set_mode chat` or `set_mode agent` | `set_mode agent` |
| Switch model | `switch_model <model_name>` | `switch_model "deepseek-v4-flash"` |

### Step 2: Panel names

Available panels and their aliases:

| Panel | Aliases |
|-------|---------|
| `documents` | library, doc, docs, document |
| `gallery` | images |
| `email` | mail, inbox, emails |
| `sessions` | chats, history |
| `notes` | (no aliases) |
| `brain` | memory, memories |
| `skills` | (no aliases) |
| `settings` | preferences |
| `cookbook` | models, serve, serving |

CRITICAL: "open memory/memories/brain" / "open skills" / "open notes" / "open documents" / "open cookbook" means OPEN THE PANEL — call `ui_control open_panel`, NOT a manage/list tool. The manage tools list contents in chat; `ui_control open_panel` opens the visual modal the user asked for.

### Step 3: Tool toggles

| Toggle name | Aliases | What it does |
|-------------|---------|--------------|
| `bash` | shell | Enables/disables bash shell commands |
| `web` | search | Enables/disables web search & fetch |
| `research` | deepresearch | Enables/disables deep research |
| `browser` | (no alias) | Enables/disables browser automation tools |
| `incognito` | (no alias) | Enables/disables incognito mode (no memory/chat search) |
| `document_editor` | documents | Enables/disables document editing tools |

### Step 4: Creating custom themes

When the user asks for a theme not in the built-in presets, use `create_theme`:
- Built-in presets: dark, light, midnight, paper, cyberpunk, retrowave, forest, ocean, ume, copper, terminal, organs, lavender, gpt, claude, cute
- For custom themes, pick distinctive, evocative hex colors that match the requested aesthetic, NOT generic defaults
- The theme auto-applies after creation

### Step 5: Opening email replies

When the user says "reply to that email" or "open a reply":
1. Find the email UID from `list_emails` / `read_email` output
2. Call `ui_control` with `action: "open_email_reply"`, `uid: <uid>`, `folder: "INBOX"`, `mode: "reply"`
- This opens the email compose window in the UI for the user to type in
- Do NOT call `reply_to_email` unless the user explicitly gives body text and wants to SEND immediately

## Pitfalls

1. **open_panel vs manage_tool:** When the user says "open <something>", they want the UI panel visible. Do NOT call a `manage_*` tool to list contents — call `ui_control open_panel`.
2. **Don't record toggle changes as memories:** When flipping a toggle, just flip it. The user doesn't want a memory that they "prefer toggles off" — the toggle state is persistent.
3. **Create_theme vs set_theme:** If the user names a built-in preset, use `set_theme`. If they describe a custom look ("make it look like a sunset"), use `create_theme` and invent a fitting name.
4. **open_email_reply vs reply_to_email:** Opening a draft compose window ≠ sending the reply. Use `open_email_reply` for drafting and `reply_to_email` only when the user explicitly says to send.

## Verification

- `ui_control open_panel skills` opens the skills panel
- `ui_control toggle bash off` disables bash (confirmed by the user)
- `create_theme` creates and auto-applies the new theme
- `open_email_reply` opens a compose window with the correct email context