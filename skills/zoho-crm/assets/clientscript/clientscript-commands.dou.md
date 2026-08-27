FILE_PURPOSE: Read when authoring a command-triggered Client Script — confirming Commands category, the 30-command cap, command-palette and per-user keyboard-shortcut trigger paths.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/commands.html
TRIGGER_KEYWORDS: Client Script Commands, Command Palette, C C shortcut, Manage Extensibility Permission, Category Commands, Keyboard Shortcuts

TECHNICAL_CONSTRAINTS:
- Commands are a Client Script category that runs anywhere in CRM, decoupled from a Module + Page binding.
- Hard cap — up to 30 Client Script Commands per CRM org.
- Default keyboard shortcut to open the Command Palette is `C C`.
- Per-user keyboard shortcuts are disabled by default; each user must enable Keyboard Shortcuts under Personal Settings before binding shortcuts to Commands.
- The "Manage" option in the per-user Commands shortcut UI is visible only to users with the `Manage Extensibility Permission` profile permission.
- Disabling or deleting a Command also deletes every keyboard-shortcut binding for that Command across all users in the org.
- Commands run "anywhere in CRM" — no page-type or module-event binding is required at creation time.

REQUIRED_PARAMETERS:
- Creation contract — when creating the Client Script, set Category to `Commands` instead of a Module; the rest of the IDE flow matches event-based scripts.
- Trigger surfaces:
    · Command Palette icon in the CRM footer (or open the palette via the `C C` shortcut), then select the Command name.
    · Per-user keyboard shortcut bound under `Setup → General → Personal Settings → Keyboard Shortcuts → Commands → Choose Command → enter Shortcut → Add shortcut`.

UI_ONLY_ACTIONS:
- Create a Command-category Client Script: `Setup → Developer Hub → Client Script → +New Script → Category = Commands → Name + Description → Next → IDE → Save and Close → toggle Enable`. Note: No API equivalent — UI-only.
- Per-user keyboard-shortcut binding: `Setup → General → Personal Settings → Keyboard Shortcuts → enable Keyboard Shortcuts → Commands section → Choose Command → enter Shortcut → Add shortcut`. Note: Bindings are per-user; no admin API.
- Admin shortcut to the Commands tab: `Personal Settings → Keyboard Shortcuts → Commands → Manage` (visible only with `Manage Extensibility Permission`). Note: No API equivalent — UI-only.

CRITICAL_FAILURE_MODES:
- Attempting to create more than 30 Commands is rejected at the cap of 30; delete an unused Command first.
- Keyboard Shortcuts disabled on a user's account → bound Command shortcut keys produce no action; verify the per-user Keyboard Shortcuts master toggle before triage.
- Disabling or deleting a Command deletes every user-bound shortcut for that Command — re-enabling the Command does not restore the bindings; users must re-bind.
- "Manage" link absent from the Commands shortcut UI → user is missing `Manage Extensibility Permission`; grant via profile before expecting admin-level Command control.
- Category mismatch — choosing Category = Module when Commands was intended routes the script under the module-event binding flow and the script becomes invisible to the Command Palette.
