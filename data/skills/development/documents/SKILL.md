---
name: documents
description: Create, edit, and manage editor documents (not disk files)
version: 1.0.0
category: development
tags: [documents, editor, writing, code]
status: published
confidence: 0.85
source: user
owner: admin
created: "2026-06-13T02:25:00Z"
---

## When to Use

Use this skill when the user wants to work with the editor — creating, editing, or managing documents. The editor is for content the user sees in a rich document panel (notes, drafts, reports, code blocks), separate from disk files.

Key phrases: "create a document", "open a doc", "write a letter", "edit this document", "save this as a document", "show me my documents", "delete that doc".

Do NOT use this skill for:
- Disk files → use `read_file` / `write_file` / `edit_file` instead
- Quick code snippets in chat → short code OK inline
- Notes → those use `manage_notes`

## Prerequisites

This skill requires these native tools:
- `manage_documents` — List, read, open, and delete editor documents
- `create_document` — Create a new editor document with content
- `edit_document` — Edit the open document by find/replace
- `update_document` — Replace the entire open document (for major rewrites)
- `suggest_document` — Suggest edits with inline accept/reject bubbles

## Procedure

### Step 1: Understand the difference

**Document tools** work on the editor in the UI — think of it like Google Docs inside Odysseus.
**File tools** (`read_file`, `write_file`, `edit_file`) work on actual disk files.

If the user says "write this to a file" → use file tools.
If the user says "create a document" or "open a doc" → use document tools.
When in doubt, check if the user wants a UI document or a disk file.

### Step 2: Choose the right action

**Creating:**
- "Create/write a document" → `create_document` with content
- If there's a lot of content (code, long text), use `create_document` instead of pasting it into chat
- Optional: pass a `title` and `language` for syntax highlighting

**Editing the open document:**
- "Fix X" / "change Y to Z" → `edit_document` with `find` and `replace` blocks
- ALWAYS use `edit_document` for small changes — never rewrite the whole doc
- Only use `update_document` for genuine full rewrites (>50% changed)

**Getting suggestions:**
- "Review this" / "give feedback" / "how can I improve this" → `suggest_document`
- Pass concrete `find`/`replace`/`reason` items
- The suggestions appear as inline accept/reject bubbles on the doc

**Managing documents:**
- "Show my documents" → `manage_documents` with `action: "list"`
- "Open a document" → `manage_documents` with `action: "open"` and the document ID
- "Delete a document" → `manage_documents` with `action: "delete"` and the ID

### Step 3: Edit patterns

For targeted edits, use `edit_document`:
```json
{
  "edits": [
    {"find": "old text to replace", "replace": "new text"},
    {"find": "another change", "replace": "the fix"}
  ]
}
```

For major rewrites, use `update_document` with the full new content:
```json
{
  "content": "entire new document content here"
}
```

## Pitfalls

1. **Document ≠ file:** Never use document tools for disk files or file tools for UI documents. They are separate systems.
2. **edit_document for small changes:** Do NOT echo back the whole file for a one-line fix. Use targeted find/replace.
3. **update_document sparingly:** Only when genuinely rewriting more than half the document. The frontend treats it as a full replacement (undo history resets).
4. **suggest_document not prose:** When the user asks for feedback, call `suggest_document` with concrete edits — do NOT write a prose list of suggestions in chat. The inline bubbles are much more useful.
5. **Adding content:** To add new content (e.g. "add a section about X"), set `find` to a short anchor snippet near where it should go, and `replace` to that same snippet PLUS the new content.

## Verification

- `create_document` returns a document ID — confirm with clickable link `[Title](#document-<id>)`
- `edit_document` shows "v2, 1 edit applied"
- `manage_documents` lists created docs
- `suggest_document` returns inline suggestions