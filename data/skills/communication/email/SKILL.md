---
name: email
description: Send, read, search, and manage email across multiple accounts
version: 1.0.0
category: communication
tags: [email, inbox, mail, accounts, gmail]
status: published
confidence: 0.85
source: user
owner: admin
created: "2026-06-13T00:55:00Z"
---

## When to Use

Use this skill when the user asks about email — reading, sending, replying, listing inbox messages, managing folders, cleaning up. This skill activates all email-related native tools and teaches the proper calling patterns.

Do NOT use this skill for notes, calendar, tasks, or scheduled jobs — those are separate skills.

## Prerequisites

This skill requires the following native tools. They are part of the `email` toolset and become available when this skill is activated:
- `list_email_accounts` — list configured mailboxes
- `list_emails` — list messages in a folder
- `read_email` — read full content of one message by UID
- `send_email` — send a new email
- `reply_to_email` — reply to an existing message by UID
- `bulk_email` — bulk delete, archive, or mark messages
- `delete_email` — delete one message by UID
- `archive_email` — archive one message by UID
- `mark_email_read` — toggle read/unread status for one message
- `resolve_contact` — look up a contact's email address by name
- `manage_contact` — manage CardDAV contacts (list, add, update, delete)

## Procedure

### Step 1: Discover accounts
When a user mentions email, FIRST call `list_email_accounts` to find which mailboxes are configured. Accounts are user-defined labels (e.g. "Gmail", "Work", "Personal"). Do NOT guess or assume — the tool output is the source of truth.

### Step 2: Choose the right action

**Listing messages:**
- "Show my inbox" → `list_emails` with `folder: "INBOX"`, `max_results: 10-20`, `unread_only: false` (include read unless asked for unread)
- "Any new mail" → `list_emails` with `unread_only: true`, `folder: "INBOX"`
- "Latest email from X" → `list_emails` with search or sender filter, `max_results: 1-5`
- "Show spam/junk" → `list_emails` with `folder: "Junk"` or `folder: "Spam"`
- "Show sent mail" → `list_emails` with `folder: "Sent"`
- For folders besides INBOX, check if the account supports them first via `list_emails` or by trying the exact folder name the user mentions

**Reading messages:**
- After listing, use the UID (value after `UID:` in output) to call `read_email` with that exact UID
- UIDs are NOT row numbers — always extract the `UID:` value from the list output

**Sending:**
- `send_email` with JSON args: `to`, `subject`, `body` (plain text), `account` (optional, defaults to primary)
- For rich HTML emails, compose the HTML body and send as a separate step

**Replying:**
- Find the UID of the message to reply to, then call `reply_to_email` with that UID and your reply body
- To draft a reply for the user to edit before sending: use `ui_control` with `open_email_reply <uid> <folder> reply` instead. This opens the email compose window in the UI. Do NOT call `reply_to_email` unless the user explicitly gives body text and wants to SEND immediately.

**Bulk actions:**
- "Delete/archive/mark all those / these 19 / the spam" → use `bulk_email` ONCE with the exact UID list from the latest `list_emails` result
- NEVER loop individual `delete_email` / `archive_email` / `mark_email_read` calls — one `bulk_email` handles the entire set
- For "mark all as read" in a folder: pass `bulk_email` with `action: "mark_read"`, `all_unread: true`, and the same `folder` + `account`
- For "delete all spam": pass `bulk_email` with `action: "delete"`, `all: true`, `folder: "Junk"`, `account: <name>`

**Contact management:**
- "Find X's email" → `resolve_contact` with the contact's name or email
- "Add a contact" → `manage_contact` with `action: "add"` and contact details
- "Update/delete a contact" → `manage_contact` with `action: "update"` or `"delete"` and the contact's UID

### Step 3: Use the correct account parameter

If the user names an account ("my Gmail", "work inbox", "personal domain"), pass the exact `account` value that `list_email_accounts` returned. If the user typo-matches a known account, use the closest listed account instead of claiming it doesn't exist.

When the user says "my inbox" or doesn't specify, the primary account is used by default. If `list_emails` output says "Other accounts" at the bottom, the user may have multiple mailboxes — mention this so they can choose.

### Step 4: Always verify success

After any write operation (send, delete, archive), check the tool result for success/failure. Do NOT claim success without confirming via the tool output. If it fails, retry with corrected parameters or tell the user what went wrong.

## Pitfalls

1. **UID vs row number:** UIDs are `UID:` values from tool output, NOT the 1‑based row numbers in the listing. Using row numbers will target the wrong message.
2. **Looping bulk actions:** Never delete/archive/mark messages one at a time — it floods context and burns through the token budget. One `bulk_email` call handles everything.
3. **Account guessing:** When the user names an account, always use the exact label from `list_email_accounts`. Never assume or use a generic name like "default".
4. **Sending before drafting:** Don't call `reply_to_email` to send if the user just wants to open a draft compose window. Use `ui_control open_email_reply` for drafts.
5. **Multiple accounts + folder discovery:** Not all accounts support arbitrary folder names. If `list_emails` with a folder name fails, tell the user what folders the account does expose (check the first listing output).

## Verification

The skill is working correctly when:
- The correct email account is always identified before reading/sending
- UIDs from `list_emails` are correctly used in subsequent `read_email` / `bulk_email` calls
- Bulk operations use a single `bulk_email` call, never individual loops
- Success/failure is confirmed from tool output, never assumed
- Draft replies use `ui_control open_email_reply`, not `reply_to_email`