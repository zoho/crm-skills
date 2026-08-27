FILE_PURPOSE: Read when implementing a common Widget coding pattern or configuring Widget deployment associations.
SOURCE_DOC: https://www.zoho.com/crm/developer/docs/widgets/usage.html, https://www.zohocrm.dev/explore/widgets/v1.5/jssdk
TRIGGER_KEYWORDS: widget-pattern, pageload-pattern, update-from-widget, search-related-widget, current-user-widget, deployment-checklist, widget-association

TECHNICAL_CONSTRAINTS:

### Pattern 1: Read record on PageLoad
```javascript
ZOHO.embeddedApp.on("PageLoad", function(data) {
    ZOHO.CRM.API.getRecord({ Entity: data.Entity, RecordID: data.EntityId })
        .then(function(record) {
            var fields = record.data[0];
            document.getElementById("name").textContent = fields.Full_Name;
            document.getElementById("email").textContent = fields.Email;
        });
});
ZOHO.embeddedApp.init();
```

### Pattern 2: Update field from widget
```javascript
ZOHO.embeddedApp.on("PageLoad", function(data) {
    document.getElementById("saveBtn").addEventListener("click", function() {
        var newValue = document.getElementById("myInput").value;
        ZOHO.CRM.API.updateRecord({
            Entity: data.Entity,
            APIData: { id: data.EntityId, Description: newValue },
            Trigger: ["workflow"]
        }).then(function() {
            ZOHO.CRM.UI.Popup.closeReload();
        });
    });
});
ZOHO.embeddedApp.init();
```

### Pattern 3: Search and display related records
```javascript
ZOHO.embeddedApp.on("PageLoad", function(data) {
    ZOHO.CRM.API.searchRecord({
        Entity: "Contacts",
        Type: "criteria",
        Query: "(Account_Name:equals:" + data.EntityId + ")"
    }).then(function(result) {
        var contacts = result.data || [];
        contacts.forEach(function(c) {
            console.log(c.Full_Name + " — " + c.Email);
        });
    });
});
ZOHO.embeddedApp.init();
```

### Pattern 4: Personalise with current user
```javascript
ZOHO.embeddedApp.on("PageLoad", function(data) {
    ZOHO.CRM.CONFIG.getCurrentUser().then(function(user) {
        document.getElementById("greeting").textContent =
            "Hello, " + user.full_name + " (" + user.profile.name + ")";
    });
});
ZOHO.embeddedApp.init();
```

### Deployment Association Paths
| Placement | Association path |
|---|---|
| **Dashboard** | Home page → Add Component → Widget |
| **Custom Button** | `Setup → Modules → {Module} → Links and Buttons → Create Button → Widget` |
| **Related List** | `Setup → Modules → {Module} → Related Lists → Create Related List → Widget` |
| **Web Tab** | `Setup → Channels → Web Tabs → Create Web Tab → Widget` |
| **Blueprint** | `Setup → Process Management → Blueprints → {Blueprint} → Transition → Attach Widget` |
| **Signal** | Signal automation config |
| **Settings** | `Setup → Developer Hub → Widgets` (Settings placement) |
| **Wizard** | `Setup → Customization → Wizards → {Wizard} → Steps` |

For Flyout widgets: register the Widget as **Custom Button type** in `Setup → Developer Hub → Widgets`.

REQUIRED_PARAMETERS:
- All `ZOHO.CRM.API.*` / `ZOHO.CRM.CONFIG.*` / `ZOHO.CRM.UI.*` calls must be inside a `PageLoad` (or equivalent) callback — SDK is not initialized before `ZOHO.embeddedApp.init()` resolves.
- `Trigger: []` in `updateRecord`/`insertRecord`/`upsertRecord` → suppresses ALL automations silently; pass explicit trigger subset (e.g. `["workflow"]`) when automation suppression is intentional.

UI_ONLY_ACTIONS:
- Widget deployment associations are configured in the CRM UI only — see Deployment Association Paths above. No API equivalent for placement association.

CRITICAL_FAILURE_MODES:
- `updateRecord`/`insertRecord`/`upsertRecord` without explicit `Trigger` array fires all workflows/blueprints/approvals; pass `Trigger: []` only when intentionally suppressing all.
- `PageLoad` not fired on Dashboard placement or direct browser access — add `setTimeout` fallback (~1500 ms) after `ZOHO.embeddedApp.init()` with a `fetchCalled` boolean guard to prevent double-invocation.
- `ZOHO.CRM.API.*` called outside a `PageLoad` callback (before `init()` resolves) → undefined or rejects.
- Flyout Widget registered as wrong type (not Custom Button) — `ZDK.Client.openWidget` flyout call silently fails.
