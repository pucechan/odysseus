---
name: notes
description: Create, edit, organize, and manage notes, checklists, and reminders
version: 1.0.0
category: communication
tags: [notes, todos, checklists, reminders]
status: published
confidence: 0.80
source: user
owner: admin
created: "2026-06-13T02:00:00Z"
---

## When to Use

Use this skill when the user asks about notes, checklists, todos, or reminders — "take a note", "remind me to X at 3pm", "make a checklist for groceries", "show my notes", "edit the shopping list note".

Do NOT use this skill for:
- User facts/preferences ("my name is X") → use `manage_memory` instead
- Recurring/scheduled tasks ("check my inbox every morning") → use `manage_tasks` instead
- Calendar events → use `manage_calendar` instead

## Prerequisites

This skill requires one native tool:
- `manage_notes` — List, add, edit, delete, and search notes with various note types (text, checklist, reminder)

## Procedure

### Step 1: Understand the note type

The user's request determines the note type:

| User says | Note type | Example |
|-----------|-----------|---------|
| "Note", "take a note", "write this down" | `text` | "Buy milk on the way home" |
| "Checklist", "list", "todos", "grocery list" | `checklist` | Items the user can check off |
| "Remind me", "set a reminder", "don't let me forget" | `reminder` | Include `due_date` for the reminder |

### Step 2: Choose the right action

**Listing notes:**
- "Show my notes" → `manage_notes` with `action: "list"`
- "Search for X in my notes" → `manage_notes` with `action: "search"` and the query

**Creating:**
- `manage_notes` with `action: "add"`, `content: "..."`, and optionally `category` / `note_type` / `due_date` (for reminders)
- For checklists, pass `note_type: "checklist"` and the content as markdown checklist items

**Editing/updating:**
- `manage_notes` with `action: "edit"` and the note ID, new content
- For surgical changes, use `action: "patch"` with old_string/new_string

**Deleting:**
- `manage_notes` with `action: "delete"` and the note ID

### Step 3: Use clickable links

- After creating or listing, render the note title as a clickable link: `[Title](#note-<id>)`

## Pitfalls

1. **Don't use manage_memory for notes:** Memory is for facts/preferences about the user ("I live in London", "call me Simone"). Notes are free-form content. Use `manage_notes`.
2. **Reminders vs tasks:** Reminders are one-off ("remind me at 3pm"). Tasks are recurring/scheduled jobs ("check inbox every morning"). Use `manage_tasks` for recurring, `manage_notes` for one-off reminders.
3. **Checklists:** When creating a checklist, include items as markdown list items in the content, e.g. `- [ ] Milk\n- [ ] Bread`. The user can check them off in the UI.
4. **Don't forget the due_date:** If the user says "remind me Friday", include `due_date: "2026-06-19T09:00:00"` (or whatever the resolved date is).

## Verification

- Note creation returns an id — confirm by saying "Saved as [Title](#note-<id>)"
- Lists show titles and previews
- Searches return relevant matches
- Deletions confirm success