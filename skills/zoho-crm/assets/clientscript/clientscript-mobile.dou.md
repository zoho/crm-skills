FILE_PURPOSE: Read when authoring a Client Script that must also run in the Zoho CRM iOS / Android mobile apps — per-page-type mobile event matrix.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/client-script/mobile.html
TRIGGER_KEYWORDS: mobile, iOS, Android, onBeforeMandatoryFormSave, beforeTransition, afterTransition, onRowAdd, onClick

TECHNICAL_CONSTRAINTS:
- Same Client Script script runs in CRM web AND CRM mobile (iOS + Android) — no separate authoring; behaviour is event-supported-or-silent on mobile.
- Mobile-supported page types: Create Page (Standard), Edit Page (Standard), Clone Page (Standard), Create Page (Wizard), Edit Page (Wizard), Detail Page (Standard), Detail Page (Canvas).
- Page types **absent** from the mobile-supported matrix: Create / Clone / Edit Page (Canvas), List Page (Standard), List Page (Canvas), Quick Create Popup. Scripts bound to those surfaces silently no-op on mobile.
- Detail Page (Standard) Blueprint events on mobile — `beforeTransition`, `afterTransition`. Note: `afterTransition` appears on mobile-Detail-Standard here but is not in the web Detail-Standard event-dictionary (eventdict-detail-standard).
- Detail Page (Canvas) on mobile is reduced — only Page `onLoad`, Mandatory Form `onBeforeMandatoryFormSave` / `onMandatoryFormLoad`, Blueprint `beforeTransition`, and Canvas Button / Icon / Text `onClick`. Subform, Notes, Tag, Field, and standard custom Button events are **not** listed for mobile Detail Canvas.

REQUIRED_PARAMETERS:
- Mobile event matrix (verbatim from source, with Type labels added for cross-reference with [clientscript-event-type-matrix.dou.md](./clientscript-event-type-matrix.dou.md)):
    · **Create / Edit / Clone Page (Standard)** — Page (Type: Page Event): `onLoad`, `onChange`, `onSave`; Field (Type: Field Event): `onChange`, `onType`; Subform (Type: Subform Event): `onCellChange`, `onRowAdd`, `beforeRowDelete`, `onRowDelete`; Custom Button (Type: Button Event): `onClick`.
    · **Create / Edit Page (Wizard)** — Wizard (Type: Wizard Event): `onLoad`, `onChange`, `onTransition`, `onBeforeTransition`, `onBeforeSave`; Field (Type: Field Event): `onChange`, `onType`; Subform (Type: Subform Event): `onCellChange`, `onRowAdd`, `beforeRowDelete`, `onRowDelete`; Custom Button (Type: Button Event): `onClick`.
    · **Detail Page (Standard)** — Page (Type: Page Event): `onLoad`; Mandatory Form (Type: Mandatory Fields Form Event): `onBeforeMandatoryFormSave`, `onMandatoryFormLoad`; Blueprint (Type: Blueprint Event): `beforeTransition`, `afterTransition`; Subform (Type: Subform Event): `onCellChange`, `onRowAdd`, `beforeRowDelete`, `beforeRowUpdate`, `onRowDelete`; Custom Button (Type: Button Event): `onClick`.
    · **Detail Page (Canvas)** — Page (Type: Page Event): `onLoad`; Mandatory Form (Type: Mandatory Fields Form Event): `onBeforeMandatoryFormSave`, `onMandatoryFormLoad`; Blueprint (Type: Blueprint Event): `beforeTransition`; Canvas Button (Type: Canvas Button Event): `onClick`; Icon (Type: Icon Event): `onClick`; Text (Type: Text Event): `onClick`.
- Sample scenario in source: Leads-record duplicate-check on save — compare other records' Email / Phone and `return false` to block save with an error message.

UI_ONLY_ACTIONS:
- *(none in source — script authoring is via Setup → Developer Hub → Client Script regardless of execution surface)*

CRITICAL_FAILURE_MODES:
- **List Page (Standard + Canvas) silent absence on mobile** — `onCustomViewLoad` / `onBeforeCustomViewChange` / `getList()` operations and per-row canvas-element clicks do not fire on the mobile List view; List-Page scripts behave as no-ops on mobile. (mobile-listpage-absent)
- **Create / Clone / Edit Page (Canvas) silent absence on mobile** — only Standard Create / Clone / Edit surfaces fire on mobile; Canvas Create / Clone / Edit scripts (including canvas Button / Icon / Text `onClick`) do not execute on mobile.
- **Quick Create absent on mobile** — Quick Create Popup events do not fire on mobile.
- **Mobile Detail-Canvas Field / Subform / Notes / Tag events silently absent** — a Detail-Canvas script with `onBeforeUpdate` (field), `onRowAdd` (subform), `onTagChanged`, or `onBeforeAdd` (notes) does not execute on mobile despite executing on web. (mobile-detail-canvas-gaps)
- **`afterTransition` (Blueprint, Detail Standard) is mobile-only per this source** — web event-dictionary does not list it; cross-surface scripts will see different Blueprint hook firing.
- **Custom Button on Detail Page Canvas absent on mobile** — only Canvas Button / Icon / Text `onClick` listed for mobile Detail-Canvas; the standard custom Button (top-bar) `onClick` is omitted.
- **Web-only ZDK UI surfaces** — Flyout / Popup / Widget-render APIs are not documented as mobile-supported in this page; cross-surface Widget invocations need explicit mobile validation.
- **Sample-scenario duplicate-check on save**: requires Web API list-records call inside `onSave`; the 10 s timeout applies on mobile networks and may abort the check.
