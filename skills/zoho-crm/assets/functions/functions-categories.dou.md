## FILE_PURPOSE
Read when selecting a Function category or writing a boilerplate Deluge function signature.

## MENTAL_MODEL
Seven categories determine return type, namespace, trigger mechanism, and argument-mapping surface. Category is set at Function creation and cannot be changed post-creation.

## WHEN_TO_USE
- Selecting the right category before writing a Deluge Function.
- Generating a boilerplate signature for any Function category.
- Verifying return type, namespace, or argument-mapping requirements.

## WHEN_NOT_TO_USE
- Writing the implementation logic inside a Function — use `zoho.crm.v8.*` or `invokeurl` DOU nodes instead.
- Configuring Function–trigger association — done at the trigger's UI surface (Workflow Rule, Button, Blueprint), not in the Function editor.

## TRIGGER_KEYWORDS
button-function, automation-function, schedule-function, related-list-function, standalone-function, sales-signals-function, validation-rule-function, category-boilerplate, crmAPIRequest, brace-on-same-line

## RULES

### Quick Reference

| Category | Return Type | Namespace | Triggered by |
|---|---|---|---|
| **Button** | `string` | `button.*` | Custom Button click |
| **Automation** | `void` | `automation.*` | Workflow Rule / Blueprint |
| **Schedule** | `void` | `schedule.*` | Time-based trigger |
| **Related List** | `string` (XML) | `related_list.*` | Related List display |
| **Standalone** | `string` | `standalone.*` | API call / Button / any caller |
| **Sales Signals** | `void` | `salessignals.*` | Signal event |
| **Validation Rule** | `map` | `validation_rule.*` | Record create/update |

- **Argument mapping**: Every argument declared in a Deluge signature must be mapped to a CRM merge variable at the trigger's UI surface (e.g. `${Deals.Id}`). An unmapped argument resolves to `null` at runtime with no error.
- **Brace format**: Opening `{` must appear on the **same line** as the function signature. Allman style (brace on next line) is rejected by the Deluge editor with "Improper code format".

## CANONICAL_EXAMPLES

### Button
```deluge
string button.FunctionName(){
    return "";
}
// With mapped argument (set at Setup → Modules → {Module} → Links and Buttons → {button} → Arguments)
string button.FunctionName(String recordId){
    return "";
}
```

### Automation
```deluge
void automation.FunctionName(){
    // CRM writes, external API calls, email sending — side-effects only
}
```

### Schedule
```deluge
void schedule.FunctionName(){
    // batch processing, sync jobs, cleanup tasks — no input arguments
}
```

### Related List
```deluge
string related_list.FunctionName(){
    // must return valid XML; CRM parses this to render the related list section
    return "<record><row no=\"0\"><FL val=\"Column\">Value</FL></row></record>";
}
```

### Standalone
```deluge
string standalone.FunctionName(){
    result = Map();
    result.put("status", "success");
    return result.toString();  // editor enforces string; serialize map/list with .toString()
}
```

### Sales Signals
```deluge
void salessignals.FunctionName(){
    // react to signal events; no return value
}
```

### Validation Rule
```deluge
map validation_rule.FunctionName(string crmAPIRequest){
    entityMap = crmAPIRequest.toMap().get("record");
    response = Map();
    if (/* validation fails */)
    {
        response.put("status", "error");
        response.put("message", "Error message — max 100 characters");
        return response;
    }
    response.put("status", "success");
    return response;
}
```

## FAILURE_MODES
- Wrong return type → runtime error; Allman brace style → editor save error "Improper code format".
- `standalone.*` declared as `map`, `list`, or `int` → editor rejects with "Invalid return Type"; always declare `string` and use `.toString()` to return structured data.
- `validation_rule.*` returns `void` or `string` → record save is NOT blocked; function silently no-ops as a validator.
- `validation_rule.*` `message` exceeds 100 characters → message may be truncated or ignored.
- Argument declared in signature but not mapped at the trigger's UI surface → resolves to `null` at runtime with no error.
- Category cannot be changed after Function creation — delete and recreate if wrong category was selected.

## RELATED_DOCS
- Execution contexts and lifecycle → [functions-overview.dou.md](./functions-overview.dou.md)
- Common coding patterns → [functions-patterns.dou.md](./functions-patterns.dou.md)
- CRM integration tasks → `assets/functions/deluge/integrations/zoho-crm/`

## SOURCE
https://www.zoho.com/crm/developer/docs/functions/overview.html
