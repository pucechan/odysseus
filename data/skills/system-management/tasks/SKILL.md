---
name: tasks
description: Create and manage recurring scheduled background AI jobs
version: 1.0.0
category: system-management
tags: [tasks, scheduled, recurring, automation, cron]
status: published
confidence: 0.80
source: user
owner: admin
created: "2026-06-13T02:10:00Z"
---

## When to Use

Use this skill when the user asks about recurring or scheduled automated tasks — "check my inbox every morning", "summarize the news daily", "remind me to water the plants every Monday", "run this every hour", "show my scheduled tasks", "stop that daily task".

Do NOT use this skill for:
- One-off reminders ("remind me at 3pm today") → use `manage_notes` instead
- Calendar events ("schedule a meeting") → use `manage_calendar` instead
- Notes or checklists → use `manage_notes` instead

## Prerequisites

This skill requires one native tool:
- `manage_tasks` — List, create, update, delete, enable/disable recurring background jobs

## Procedure

### Step 1: Recognize recurring requests

The user may not say "task" explicitly. Watch for these patterns:
- "Every morning/day/week/month" → recurring task
- "Daily/automatically/scheduled" → recurring task
- "On a schedule/at regular intervals" → recurring task
- "Keep doing X" or "always X" → possibly a recurring task

### Step 2: DO NOT just do it once

If the user says "check my inbox every morning", do NOT check their inbox right now and declare it done. The user wants it to RECUR. Call `manage_tasks` with `action: "create"` to set up the schedule. Optionally, AFTER creating, you may do a one-time sample run and show the result — but the primary action is creating the task.

### Step 3: Choose the right action

**Creating a task:**
- `manage_tasks` with `action: "create"`
- `prompt` — what to do (be specific, include the full instructions the task should follow)
- `schedule` — human-readable description like "every morning at 8am"
- `cron` — optional cron expression for precise scheduling (e.g. "0 8 * * *")

**Listing tasks:**
- "Show my tasks" / "what's scheduled" → `manage_tasks` with `action: "list"`

**Updating:**
- `manage_tasks` with `action: "edit"`, the task ID, and fields to change

**Enabling/disabling:**
- "Pause the daily email check" → `manage_tasks` with `action: "disable"`, the task ID
- "Resume it" → `manage_tasks` with `action: "enable"`, the task ID

**Deleting:**
- `manage_tasks` with `action: "delete"`, the task ID

### Step 4: Use clickable links

- Render tasks as clickable links: `[Task name](#task-<id>)`
- After creating: "Created [Daily inbox summary](#task-abc123) — it'll run every morning at 8am and show results in the Tasks panel"

## Pitfalls

1. **Don't do it inline:** When the user asks for something recurring, do NOT just perform the action once. Create the task. The user can see results in the Tasks panel.
2. **Tasks vs notes:** `manage_tasks` is for recurring background AI jobs. `manage_notes` with `due_date` is for one-off reminders. Don't confuse them.
3. **Vague schedules:** If the user says "do X regularly" without specifics, ask "How often? Every morning, weekly, something else?"
4. **Task prompt specificity:** The prompt should be self-contained — the task runs without human supervision, so include all necessary context ("check my Gmail inbox for unread from my boss and summarize", not just "check email").
5. **Don't forget to confirm:** After creating, tell the user when it'll run and that results appear in the Tasks panel. Include the clickable link.

## Verification

- Created task appears in `manage_tasks action=list`
- Disabled tasks show as inactive in the list
- Deleted tasks no longer appear
- The user sees results in the Tasks panel at the scheduled time