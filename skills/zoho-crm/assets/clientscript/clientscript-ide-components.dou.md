FILE_PURPOSE: Read when working inside the Client Script IDE — Code Editor / Review / Revisions / Run / Settings panels, API-name autocomplete, log + Terminal usage, and the 30-revision history cap.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/ide-components.html
TRIGGER_KEYWORDS: Client Script IDE, ZDK.client.showMessage, Revisions, Terminal, Messages panel, Run, Commit Message, Hard Reload

TECHNICAL_CONSTRAINTS:
- IDE provides syntax highlighting, smart code completions, JavaScript + ZDK definitions, and auto-suggestion of module / field API names whenever a single or double quote is entered.
- Single-line comment syntax `//`; block comment syntax `/* ... */`.
- On Save, if the editor finds an error, an error panel listing the errors pops up at the bottom; the error icon on the status bar (bottom-right) reopens the panel.
- Information section (right pane) shows page + event details, a Commit Message field, and a Library help icon that opens ZDK documentation.
- Static Resources section (right pane, below Information) lists the org's uploaded static resources for one-click Add into the current script; see [clientscript-static-resources.dou.md](./clientscript-static-resources.dou.md).
- Run mode executes the script live — CRM operations performed in Run mode persist in the live CRM account (no sandbox isolation inside Run).
- Run panel exposes Reload and Hard Reload of the underlying CRM tab for retesting.
- Messages panel under Run logs execution metadata: event + script details, execution status, logs, exception messages, and execution time.
- Terminal panel under Run accepts ad-hoc ZDK statements (e.g. `ZDK.client.showMessage('Welcome to Client Script IDE', { type: 'info' })`) and executes them on Enter.
- Revisions panel keeps up to 30 saved versions of a script with commit messages; the "Use this revision" action on a revision rolls the script back to that version.
- Review (Save) flow opens a diff editor; on save, if the server has a newer version of the script, the latest source and the local source are presented for conflict-resolution review.
- Status bar shows the last-modifying user and provides a Full-screen toggle and a Feedback icon for submitting event / ZDK API feedback to Zoho.
- Settings panel customizes Theme (Dark / Light), Cursor, Format (auto-format on paste / on type), Font, Minimap, Word Spacing, Selection (drag-to-move), Find, Suggestion (Insert vs Replace), Brackets (default = highlight all matching).

REQUIRED_PARAMETERS:
- IDE entry — opens automatically on `Next` from the Create Script pop-up; subsequently via `Setup → Developer Hub → Client Script → {script} → Edit`.
- Per-save inputs — script body (Code Editor) + optional Commit Message (Information section).
- Terminal contract — any valid ZDK expression evaluated on Enter; observed result printed inline.

UI_ONLY_ACTIONS:
- Open the IDE for an existing script: `Setup → Developer Hub → Client Script → {script} → Edit`. Note: No API equivalent — UI-only.
- View or restore a prior revision: IDE → Revisions panel → select revision → `Use this revision`. Note: No API equivalent — UI-only.
- Submit feedback on events / ZDK APIs: IDE status bar → Feedback icon. Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- Run-mode CRM operations are not sandboxed — running a script that writes to records mutates live CRM data; guard with explicit test records.
- Revision history caps at 30 — older saves drop off; tag important versions in the Commit Message so the right revision can be located before drop-off.
- Save-time conflict — when another author updated the same script concurrently, the diff editor opens; choosing the wrong side overwrites the other author's edit. (conflict-management)
- Editor error panel pops up only when Save finds errors — runtime errors surface only in the Run → Messages panel; relying on the Save-time error panel for runtime issues misses them.
- Settings (Theme / Font / Minimap / etc.) are per-user IDE preferences; they do not change script behavior, so do not rely on Settings parity across authors during debugging.
