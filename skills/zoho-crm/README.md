# zoho-crm

> Zoho CRM v8.0 orchestration layer — primitive selection, code generation, and validation across all CRM developer tools: REST API, Deluge Functions, ClientScript, Widgets, COQL, Queries Workbench, and Connections.

This repository hosts the `SKILL.md` file for **zoho-crm**, a portable Agent Skill you can drop into any compatible harness (Claude Code, Codex CLI, Cursor, Claude Desktop, and other agents that support the `SKILL.md` convention).

> **Note:** This `README.md` is for human visitors browsing GitHub. It is separate from `SKILL.md`, which the agent actually loads — do not put installation instructions inside `SKILL.md` itself.

## What's inside

```
zoho-crm/
├── SKILL.md          # Routing logic, primitive selection, and 5-step reasoning flow
├── references/       # Subskill files per primitive (api, functions, clientscript, widgets, coql, queries, connections)
└── assets/           # DOU nodes — authoritative method signatures, parameters, and failure modes
    ├── api/
    ├── functions/
    ├── clientscript/
    ├── widgets/
    ├── coql/
    ├── queries/
    └── connections/
```

The current version is tracked in the YAML frontmatter of `SKILL.md`:

```yaml
---
name: zoho-crm
description: 'Zoho CRM v8.0 orchestration layer...'
metadata:
  version: "0.0.1"
---
```

## Quick install (recommended)

The fastest way to install this skill is the community `skills` CLI — no `git clone` needed, it fetches the folder straight from GitHub and places it in the right directory for your agent:

```bash
npx skills add zoho/crm-skills --agent claude-code
```

Replace `claude-code` with the identifier of your preferred [supported agent](https://github.com/vercel-labs/skills#supported-agents). You can also use `--agent '*'` to install the skill for all supported agents. 

Add `-g` to install it globally (available in every project) instead of just the current repo:

```bash
npx skills add zoho/crm-skills -g
```

Restart your agent session after adding a skill to ensure the new skill is discovered and available. Some agents may support live reloading of skills without a restart.

To remove this skill from all agents in the current project scope:

```bash
npx skills remove zoho-crm --all
```

## Upgrading with the CLI

Skills don't auto-update. Run either of these when you want the latest version:

```bash
# Update every skill installed via the CLI to its latest version
npx skills update

# Or re-add this one skill explicitly to force a refresh
npx skills add zoho/crm-skills --agent claude-code
```

If you're pinning versions for a team or CI environment, restore from the lockfile instead so everyone stays on the exact same version:

```bash
npx skills experimental_install
```

To check what's currently installed and its pinned version:

```bash
npx skills list
```

> **Tip:** `npx skills` can occasionally run a stale cached CLI version. If an update doesn't seem to take effect, force the latest CLI itself with `npx skills@latest update`.

## Checking your currently installed version

Whether you installed via the CLI or by hand, the source of truth is the `version` field in the installed `SKILL.md`'s frontmatter:

```bash
head -n 10 ~/.claude/skills/zoho-crm/SKILL.md
```

Compare it against the latest tag on this repo's [Releases page](https://github.com/zoho/crm-skills/releases).

## Manual install / upgrade (no Node.js required)

If Node.js isn't available, a skill is just a folder — plain git or a ZIP download both work.

**Option A — Re-clone and overwrite (recommended)**

```bash
git clone https://github.com/zoho/crm-skills.git /tmp/skill-update
rm -rf ~/.claude/skills/zoho-crm
cp -r /tmp/skill-update/zoho-crm ~/.claude/skills/zoho-crm
```

**Option B — Pull if you cloned the repo directly into your skills folder**

```bash
cd ~/.claude/skills/zoho-crm
git pull origin main
```

**Option C — Pin to a specific release tag** (safer for production — avoids picking up unreleased changes on `main`)

```bash
git clone --branch v0.0.1 https://github.com/zoho/crm-skills.git ~/.claude/skills/zoho-crm
```

Or use GitHub's **Code → Download ZIP** button and extract the `zoho-crm` folder directly into your agent's skills directory (see the path table below).

After any manual copy, restart your harness (or hot-reload if your harness supports it) so it picks up the updated `SKILL.md`.

## Skills directory by agent

| Agent | Personal / global path | Project path |
|---|---|---|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.codex/skills/` | `.codex/skills/` |
| Cursor | `~/.cursor/skills/` | `.cursor/skills/` |
| Claude Desktop | Settings → Capabilities → Skills (upload) | n/a |
| GitHub Copilot / Windsurf / others | `~/.agents/skills/` | agent-specific subfolder (e.g. `.windsurf/skills/`) |

## Verifying the upgrade worked

1. Re-check the `version` field in the installed `SKILL.md` — it should match the version you just installed.
2. Ask your agent something that exercises the skill and confirm the new behavior is in effect.
3. Fully restart your agent session — most harnesses read skill metadata only once at startup, so a stale session is the most common reason an upgrade "doesn't take."

## Versioning policy

This project follows [semantic versioning](https://semver.org/):

- **Patch** (`0.0.1` → `0.0.2`) — wording / clarity fixes, no behavior change.
- **Minor** (`0.0.1` → `0.1.0`) — new capabilities, backward compatible.
- **Major** (`0.0.1` → `1.0.0`) — breaking changes to expected inputs or behavior; re-read the skill instructions before upgrading.

Check the [CHANGELOG](./CHANGELOG.md) before upgrading across a major version bump.

## Troubleshooting

- **Agent doesn't see the skill at all:** confirm the folder name is `zoho-crm` (matching the `name` field exactly) and that it sits directly under the agent's skills directory — not nested one level too deep, a common ZIP-extraction artifact.
- **Old behavior persists after upgrade:** fully restart your agent session; skill metadata is typically cached for the session.
- **`npx skills` installs an old version:** run `npx skills@latest add ...` to bypass a stale cached CLI version.
- **YAML parse errors:** validate that frontmatter is fenced by `---` on its own line at the very top and bottom of `SKILL.md`, with no tabs (YAML requires spaces).
