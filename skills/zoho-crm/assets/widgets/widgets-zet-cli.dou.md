FILE_PURPOSE: Read when installing the zet CLI and running the init / run / validate / pack lifecycle to scaffold, serve, lint, and zip a CRM Widget locally.
SOURCE_DOC: widgets/install-cli.md
TRIGGER_KEYWORDS: zet init, zet run, zet validate, zet pack, zoho-extension-toolkit, plugin-manifest.json, localhost:5000, app/widget.html, dist/

TECHNICAL_CONSTRAINTS:
- Host runtime — Node.js + npm; verify with `node -v` and `npm -v` before installing the toolkit.
- `zet` ships as the global npm package `zoho-extension-toolkit`; bare `zet` invocation prints the help banner on successful install.
- `zet run` binds plain HTTP on port 5000 of the local machine; URL is reachable only from the host machine (not from LAN peers).
- **Port override**: `zet run` has no `--port` CLI flag, but the port is controlled by `var port = 5000;` on line ~19 of `server/index.js` inside the project folder. Change that value to any free port (e.g. `3000`) before running `zet run` to serve on a different port. The local URL becomes `http://127.0.0.1:<port>/app/widget.html`.
- Endpoints served — `app/widget.html` at `http://127.0.0.1:5000/app/widget.html`; manifest at `http://localhost:5000/plugin-manifest.json`.
- `zet validate` enforces manifest shape and required asset paths — it does not lint application JS / HTML / CSS for correctness.
- `zet pack` writes `dist/<project>.zip` (overwritten on re-pack); `dist/` is ephemeral build output and belongs in `.gitignore`.
- `zet validate` and `zet pack` are pure-local; neither contacts Zoho servers; no CRM credentials are required by any `zet` subcommand.
- Project layout — assets under `app/`, entry `widget.html`, descriptor `plugin-manifest.json` at project root; renaming `app/` breaks `zet run` and `zet pack` unless manifest is updated in lockstep.
- Scaffold targets the service chosen at `zet init` time; choosing a non-CRM service produces a different SDK CDN tag and manifest schema.
- `zet init` writes the scaffold into `<cwd>/{Project_name}/`; running `zet init` inside an existing project directory creates a nested project, not an upgrade.
- `app/widget.html` is the default entry name expected by `plugin-manifest.json`; renaming the entry without manifest edit breaks both `zet run` and the in-CRM Index URL.
- `zet validate` reads `plugin-manifest.json` to determine required asset paths; missing referenced assets fail validation.

REQUIRED_PARAMETERS:
- Install — `npm install -g zoho-extension-toolkit`.
- Scaffold — `zet init` → select Zoho CRM service → project name → `cd {Project_name}`.
- Serve — `zet run`; verify at `http://127.0.0.1:5000/app/widget.html`.
- In-CRM dev-loop testing — register a Widget with **External Hosting** in the sandbox (or production) account and set its Base URL to the `zet run` URL (`http://127.0.0.1:5000/app/widget.html`); the host machine renders the live local bundle inside CRM without re-packing on every edit. Only the developer's own browser can reach the local URL; switch back to Internal Hosting + `zet pack` before shipping to teammates.
- Validate — `zet validate`; resolve every violation before packing.
- Pack — `zet pack`; emits `<project>/dist/<project>.zip`, the only accepted artefact for Internal-hosting upload (see [widgets-usage.dou.md](./widgets-usage.dou.md)).

UI_ONLY_ACTIONS:
- Install Node.js on the host before `npm install -g zoho-extension-toolkit`. Note: No API equivalent — host-machine setup.
- Upload the `dist/<project>.zip` to CRM — see [widgets-usage.dou.md](./widgets-usage.dou.md) for the full `Setup → Developer Hub → Widgets` Internal-hosting flow.

CRITICAL_FAILURE_MODES:
- Port 5000 occupied: `zet run` bind fails. Do NOT kill the existing process. Instead, open `server/index.js` in the project folder, change `var port = 5000;` to any free port (e.g. `var port = 3000;`), then re-run `zet run`. The widget will be served on the new port.
- `zet validate` violations left unresolved before `zet pack`: produced `.zip` is rejected by the Developer Console upload.
- Wrong service chosen at `zet init` (Creator / Desk / Books instead of CRM): rebuild the project rather than hand-editing the SDK / manifest.
- Toolkit installed without `-g`: `zet` not on `PATH` — reinstall with `-g` or invoke via `npx zoho-extension-toolkit`.
- Node.js major-version upgrade without reinstall: native binding mismatch — rerun `npm install -g zoho-extension-toolkit`.
- `plugin-manifest.json` and `app/widget.html` edited out of lockstep: `zet validate` fails.
- Local-serve URL configured as a production External-hosting Base URL: only the host machine can reach it — every other user sees a blank Widget. (See [widgets-usage.dou.md](./widgets-usage.dou.md) for the HTTPS hosting contract.)
- `dist/` committed to source control: stale `.zip` shipped to teammates — treat as build output only.
- `zet pack` run without saving recent edits to `app/widget.html`: the archive ships the previous on-disk version — save all files before packing.
- Validation passed on developer machine but upload fails in another environment: confirm the same toolkit version with `zet --version` before triage.
- `zet init` chosen project name containing spaces or special characters: downstream npm / shell tooling breaks — use kebab-case or snake_case identifiers.
- `zet pack` archive contains hidden `.DS_Store` / `.git/` payload because the project was packed without cleanup: Developer Console upload risks rejection — prune before pack.
- Browser cache holding the previous `widget.html` bundle even after page reload: clear site data for the CRM origin to force fetch.
- Two `zet run` invocations in parallel on the same project: second fails to bind port 5000 — run a single serve at a time.
- `npm install -g zoho-extension-toolkit` permission errors on macOS / Linux without a Node version manager: switch to nvm / fnm rather than `sudo`-installing globally.
- `zet pack` output `.zip` opened, edited in-place, and re-zipped manually: invalidates the manifest contract — always re-run `zet pack` after source edits.
- Project moved across machines without committing `plugin-manifest.json`: `zet run` and `zet pack` lose the entry / asset wiring — always version-control the manifest.
- `localhost` vs `127.0.0.1` mismatch when wiring the dev URL into CRM External hosting: pick one host and use it consistently to avoid CORS surprises in some browsers.
- Toolkit upgraded mid-project without rerunning `zet validate`: legacy manifest fields silently deprecate — re-validate after every CLI upgrade.
- Anti-virus / endpoint-protection software quarantining the packed `.zip`: confirm the archive size on disk matches what gets uploaded.
