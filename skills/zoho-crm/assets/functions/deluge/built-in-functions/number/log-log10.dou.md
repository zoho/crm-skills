FILE_PURPOSE: Deluge `log()` / `log10()` — compute the natural or base-10 logarithm of a number.
MENTAL_MODEL: `n.log()` = ln(n) as DECIMAL; `n.log10()` = log₁₀(n) as DECIMAL; both return null for n ≤ 0.

WHEN_TO_USE:
- Compute the natural logarithm (ln) for mathematical or statistical operations (log).
- Compute the base-10 logarithm for scale or magnitude calculations (log10).

WHEN_NOT_TO_USE:
- When input is ≤ 0 — both functions return null silently instead of throwing an error.

TRIGGER_KEYWORDS:
log(), log10(), natural-logarithm, base-10-log, null-nonpositive, ln-inverse-exp

RULES:
- `log()` return type: DECIMAL; input: NUMBER or DECIMAL; computes natural logarithm (ln, base e).
- `log10()` return type: DECIMAL; input: NUMBER or DECIMAL; computes base-10 logarithm.
- Both functions return null when input ≤ 0 (no runtime error).
- `log()` accepts two syntaxes: `<num>.log()` / `log(<num>)`.
- `log10()` accepts two syntaxes: `<num>.log10()` / `log10(<num>)`.

CANONICAL_EXAMPLES:
```deluge
number = 90;
logValue = number.log();        // returns 4.499809670330265 (natural log)

number = 81;
info number.log10();            // returns 1.9084850188786497 (base-10 log)

info (0).log();                 // returns null (input ≤ 0)
info (-5).log10();              // returns null (input ≤ 0)
```

FAILURE_MODES:
- Input ≤ 0 returns null silently for both log() and log10() — no runtime error is raised.

RELATED_DOCS:
- exp — exp.dou.md
- Number functions — https://www.zoho.com/deluge/help/functions/number.html

SOURCE:
https://www.zoho.com/deluge/help/functions/number/log.html, https://www.zoho.com/deluge/help/functions/number/log10.html
