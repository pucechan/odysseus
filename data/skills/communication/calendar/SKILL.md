---
name: calendar
description: Manage calendar events — view, create, update, and delete events
version: 1.0.0
category: communication
tags: [calendar, events, schedule, appointments]
status: published
confidence: 0.80
source: user
owner: admin
created: "2026-06-13T02:05:00Z"
---

## When to Use

Use this skill when the user asks about calendar events, appointments, meetings, or scheduling — "what's on my calendar today", "add an event", "schedule a meeting", "reschedule my dentist appointment", "delete the 3pm meeting".

Do NOT use this skill for:
- One-off reminders ("remind me at 3pm") → use `manage_notes` instead
- Recurring tasks ("check my inbox every morning") → use `manage_tasks` instead
- Notes or checklists → use `manage_notes` instead

## Prerequisites

This skill requires one native tool:
- `manage_calendar` — List, create, update, and delete calendar events. Always call list_calendars first.

## Procedure

### Step 1: List calendars FIRST

Before any create, update, or delete operation, ALWAYS call:
```
manage_calendar action=list_calendars
```
This discovers available calendars and their IDs. Never assume calendar names or IDs.

### Step 2: Resolve dates

The system provides the current date and time. Resolve relative dates:
- "today" / "tonight" → current date
- "tomorrow" → current date + 1 day
- "next Monday" / "Friday" → next occurrence of that day
- "next week" → current date + 7 days
- Time: "3pm" / "15:00" → use 24h format in ISO 8601

Pass ISO 8601 datetimes in the user's local wall time.

### Step 3: Choose the right action

**Viewing events:**
- "What's on my calendar" / "show events" → `manage_calendar` with `action: "list"`, `start_date` and `end_date` for the requested range
- Default to today/tomorrow if no range specified
- Pass the calendar ID from step 1 if the user has multiple calendars

**Creating events:**
- `manage_calendar` with `action: "create"`, `summary`, `start` (ISO 8601), `end` (ISO 8601)
- Optional: `description`, `location`, `calendar_id` (from step 1), `all_day` (boolean), `reminder_minutes`
- For all-day events, set `all_day: true` and pass YYYY-MM-DD dates

**Updating events:**
- Get the event UID from a list or creation result
- `manage_calendar` with `action: "update"`, `uid`, and the fields to change

**Deleting events:**
- Get the event UID from a list result
- `manage_calendar` with `action: "delete"`, `uid`

### Step 4: Use clickable links

- Render events as clickable links: `[Summary](#event-<uid>)` — opens the calendar on that day
- After creating: "Added [Meeting with team](#event-abc123) for tomorrow at 2pm"

## Pitfalls

1. **Always list calendars first:** The very first call must be `action=list_calendars`. Calendars can have user-defined names and the tool needs to know which one to use.
2. **Time zones:** The system provides the current time. For "at 3pm", use the user's local time — do not convert to UTC unless the user specifies.
3. **All-day events:** For "all day Friday", use `all_day: true` with YYYY-MM-DD dates, not datetime strings.
4. **Reminders:** If the user asks for a reminder on an event, use `reminder_minutes` in the create/update call. The tool creates the note reminder — do NOT call `manage_notes` separately.
5. **Calendar ID persistence:** If the user has multiple calendars ("work", "personal"), remember which one was used for subsequent operations in the same conversation.

## Verification

- `list_calendars` returns at least one calendar with a name
- Created events appear in subsequent list calls
- Updates reflect the changed fields
- Deletions confirm the UID was removed