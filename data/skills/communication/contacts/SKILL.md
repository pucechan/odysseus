---
name: contacts
description: Look up, add, update, and delete address-book contacts using resolve_contact and manage_contact.
version: 1.0.0
category: communication
tags: [contacts, address-book, carddav, phone, email, people]
status: published
confidence: 0.90
source: user
owner: admin
created: "2026-06-26T21:05:00Z"
---

## When to Use

Use this skill when the user asks about another person's contact details or wants to save/update/delete an address-book contact.

Typical requests:

- "What is Chris's email address?"
- "Find Mum's phone number."
- "Add Alice to my contacts."
- "Save this address for Bob."
- "Update Jane's mobile number."
- "Delete the old contact for Sam."

Do **not** use this skill for:

- Durable facts about the user themselves, such as "my name is Simone" or "I prefer dark mode" — use `manage_memory`.
- Notes/reminders/tasks about people — use `manage_notes` or `manage_tasks` as appropriate.
- Sending email once the recipient is resolved — use email tools after contact lookup.

## Prerequisites

This skill uses native tools:

- `resolve_contact` — look up a person's email/phone/address by name from the address book and sent email history.
- `manage_contact` — list, add, update, or delete CardDAV/address-book contacts.

## Procedure

### Step 1: Classify the request

Use `resolve_contact` for lookup requests:

- "Find X's email"
- "What's X's phone?"
- "Who is in my contacts called X?"

Use `manage_contact` for address-book management:

- list contacts
- add a new contact
- update an existing contact
- delete a contact

### Step 2: Look up contacts safely

For lookup, call `resolve_contact` with the person's name or known email/phone fragment. Use the tool result as source of truth.

If multiple people match, present the likely matches and ask which one the user means.

### Step 3: Add contacts

For a new contact, extract available fields:

- name
- email
- phone numbers
- postal address
- notes/context if supported

Call `manage_contact` with `action: "add"` and the fields. If a required name or contact detail is missing, ask one concise clarification question.

### Step 4: Update or delete contacts

For update/delete, first identify the contact UID. If the UID is not already known, call `manage_contact` with `action: "list"` or lookup/search if supported.

Then call:

- `manage_contact` action `update` with the UID and changed fields
- `manage_contact` action `delete` with the UID

For deletion or replacing important details, confirm if the target is ambiguous.

### Step 5: Use contact results with email tools when needed

If the user's goal is to send an email to a named person:

1. Resolve the contact first if the email address is not already known.
2. Then use `send_email` or `ui_control open_email_reply` / email tools depending on the request.

## Pitfalls

- **Do not store address-book data in memory.** Email addresses, phone numbers, and postal addresses for other people belong in contacts.
- **Do not use contacts for user identity facts.** "My name is X" is memory, not a contact.
- **UIDs matter for update/delete.** List or resolve first; do not guess.
- **Handle duplicate names carefully.** Ask when multiple contacts match.
- **Do not invent contact details.** If lookup fails, say you could not find the contact.

## Verification

- Lookups return the correct person/details from tool output.
- Added contacts appear in `manage_contact action=list`.
- Updated contacts show the new details.
- Deleted contacts no longer appear.
