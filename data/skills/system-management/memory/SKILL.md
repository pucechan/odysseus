---
name: memory
description: Manage persistent user memory — durable facts and preferences about the user
version: 1.0.0
category: system-management
tags: [memory, facts, preferences, user-facts]
status: published
confidence: 0.90
source: user
owner: admin
created: "2026-06-13T02:40:00Z"
---

## When to Use

Use this skill to read, write, and manage the user's persistent memory. Memory stores durable facts and preferences about the user that should persist across sessions.

Key phrases: "remember that I...", "my name is...", "I live in...", "I prefer...", "call me...", "save that", "what do you know about me", "forget that", "update my preference".

Do NOT use this skill for:
- Notes, checklists, reminders → use `manage_notes` instead
- Contacts, phone numbers, email addresses, or postal addresses for other people → use `resolve_contact` / `manage_contact` instead
- Recurring tasks → use `manage_tasks` instead

## Prerequisites

This skill requires one native tool (always available):
- `manage_memory` — List, add, edit, delete, and search memories

## Procedure

### Step 1: Recognize what to memorize

When the user shares:
- Personal facts: "my name is Simone", "I live in London", "I'm a developer"
- Preferences: "I prefer concise replies", "I like dark mode", "call me honey"
- Important personal dates: "my birthday is June 15"
- Recurring context: "I work from home", "I have three cats"

Call `manage_memory` with `action: "add"`, the fact as `text`, and optionally a `category`.

Categories help organize memories:
- `personal` — name, location, birthday, family
- `preferences` — communication style, likes/dislikes
- `work` — job, employer, skills
- `event` — important personal dates or milestones

### Step 2: Choose the right action

**Adding:**
- `manage_memory` with `action: "add"`, `text: "The user's name is Simone"`, `category: "personal"`
- Make the text self-contained and specific — not vague

**Reading/listing:**
- "What do you know about me" → `manage_memory` with `action: "list"` (optionally `category` to filter)
- Show the user what you know in a friendly, organized way

**Searching:**
- "Where do I live" → `manage_memory` with `action: "search"` and the query
- Prefer search over list when the user asks about a specific thing

**Updating:**
- If the user corrects a fact ("actually I live in Manchester, not London"): `manage_memory` with `action: "edit"`, the `memory_id`, and corrected `text`
- OR `action: "delete"` the old one, then `action: "add"` the new one

**Deleting:**
- "Forget that" / "delete that memory" → `manage_memory` with `action: "delete"` and the `memory_id`
- Find the ID by listing or searching first

### Step 3: Be proactive

If the user shares a fact naturally in conversation ("I love Italian food" / "my dog's name is Luna"), memorize it! You don't need to ask permission — just save it and say "Got it, I'll remember that!"

## Pitfalls

1. **Memory ≠ notes:** Notes are for the user to read. Memory is for YOU to remember. Don't use `manage_memory` for note content, and don't use `manage_notes` for user facts.
2. **Never use manage_contact for user facts:** "my name is X" → `manage_memory`. `manage_contact` is only for contacts with email/phone that you might email or call.
3. **Be specific in memory text:** "The user prefers concise replies" is better than "preferences" — the text should be useful when retrieved later.
4. **Update, don't duplicate:** If the user changes a fact you already know, edit or delete+add rather than adding a contradictory memory.
5. **Don't clutter with trivial memories:** "The user is currently wearing blue socks" — use judgment. Only memorize things that are likely to be referenced again.

## Verification

- Added memories appear in subsequent `manage_memory action=list` results
- Searches find relevant memories
- Edits update the text correctly
- Deletions remove the memory from future queries