---
name: background-jobs
description: Inspect output from detached bash jobs and stop runaway background jobs started by the agent.
version: 1.0.0
category: system-management
tags: [background-jobs, bash, shell, long-running, manage_bg_jobs]
status: published
confidence: 0.85
source: user
owner: admin
created: "2026-06-26T21:05:00Z"
---

## When to Use

Use this skill when the user asks about a detached/background bash job that was started by the agent, especially jobs launched with the `#!bg` marker.

Typical requests:

- "Is that background job done?"
- "Check the build output."
- "Show me the output from the job."
- "Kill that background job."
- "Stop the runaway process."
- "List background jobs."

Do **not** use this skill for:

- Scheduled recurring AI tasks — use `manage_tasks` instead.
- Cookbook model servers — use Cookbook tools such as `list_served_models` / `stop_served_model` instead.
- General OS process hunting unless the user explicitly asks for shell-level investigation and shell is available.

## Prerequisites

This skill requires the native tool:

- `manage_bg_jobs` — list, inspect output from, or kill detached bash jobs scoped to the current chat/session.

## Procedure

### Step 1: List jobs first when no job id is known

If the user says "the job" or "that background job" and no job id is visible in recent context, call `manage_bg_jobs` with `action: "list"`.

Use the returned job ids for follow-up actions.

### Step 2: Inspect output/status

For requests like "is it done", "check output", "show logs", or "what happened", call `manage_bg_jobs` with:

- `action: "output"`
- `job_id`: the id from `list`

Then summarize:

- whether it is running, finished, failed, or killed
- the important output/error lines
- any obvious next step

### Step 3: Stop a job when requested

For "kill", "stop", "cancel", or "terminate", call `manage_bg_jobs` with:

- `action: "kill"`
- `job_id`: the exact job id

If multiple running jobs match, ask which one or list the jobs and explain the choices.

### Step 4: Avoid re-running work unnecessarily

If the user asks for status/output, inspect the existing job. Do not start a new bash command unless the existing job output shows that a new action is needed.

## Pitfalls

- **Background jobs are not scheduled tasks.** `manage_bg_jobs` is for detached bash jobs in the current chat, not recurring task automation.
- **Do not guess job ids.** List jobs if unsure.
- **Do not kill ambiguous jobs.** Ask or list first when multiple jobs could match.
- **Do not use Cookbook stop tools for normal bash jobs**, and do not use `manage_bg_jobs` for Cookbook servers.
- **Report failures plainly.** If the registry says there is no active job, tell the user rather than pretending to have checked it.

## Verification

- `list` shows the job before output/kill when needed.
- `output` returns the captured logs/status.
- `kill` reports success or a clear failure.
- The final answer names the job/status and the relevant result.
