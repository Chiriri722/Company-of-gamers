# Local CLI compatibility

Company of Gamers keeps the original `.claude/` prompts, templates and helpers
as its content source. The portable `studio` skill reads one workflow at a time
through `scripts/studio.py`. No provider SDK, API key, model mapping, global
installation, or generated copy of the 74 workflows is required.

## First-wave entrypoints

Start the installed, authenticated CLI **at the repository root**. Enable project
skills using that CLI's normal workspace trust flow.

| Host | Launch | Skill location | Example inside the session |
|---|---|---|---|
| Codex CLI | `codex` | `.agents/skills/studio/` | `$studio start` |
| Antigravity CLI | `agy` | `.agents/skills/studio/` | `/studio start` |
| Muse Code | `muse` | `.agents/skills/studio/` | Select `studio` in `/skills`, then request `start` |
| Grok Build | `grok` | `.grok/skills/studio/` | `/studio start` (or `/skills studio`, then request `start`) |
| pi | `pi` | `.agents/skills/studio/` | `/skill:studio start` |

The universal text request is: **Read `.agents/skills/studio/SKILL.md` and run
the `start` workflow.** It also works if command discovery is disabled or a
client reserves a slash command. `studio` without a workflow selects `help`.
`studio list` lists the catalog. Workflow arguments follow its name, for example
`studio setup-engine godot 4.6` or `studio team-combat melee parry --review solo`.

Only `studio` is registered natively by this adapter. The 74 original commands
are routed through it; this does not install 74 separate slash commands or 49
native subagent registrations. Muse and Grok may also discover the original
Claude skills: choose `studio` to get the portable translation.

## Runtime contract

1. Load `AGENTS.md` and the selected workflow, not every prompt at session start.
2. `python scripts/studio.py skill <name>` **prints instructions only**. It strips
   Claude frontmatter and converts standalone shell-injection lines into explicit
   Bash steps. The agent must run those steps and consume their actual output.
   It must not interpret "Resolved above" as proof a command ran.
3. All commands run from the root. The renderer replaces Claude directory
   variables with paths to the original content. Relative supporting files
   remain relative to `.claude/skills/<name>/`, not `.agents/skills/studio/`.
   Use `python scripts/studio.py reference <name> references/<file>.md` to load
   supporting files with the same translation. Never evaluate `$ARGUMENTS` as
   shell code; keep the user's text in conversation.
4. Translate nested `/workflow` handoffs into `studio workflow` with the same
   arguments. Honor explicit-only workflows (such as `story-done`) and the
   user's scope rather than automatically invoking them from a suggestion.
5. Honor missing capabilities: report `NOT ASSESSED` / `BLOCKED` for a required
   check that could not run. No fallback may manufacture approvals, independent
   reviews, test evidence, screenshots, or successful hook execution.

### Tools and roles

| Original instruction | Portable behavior |
|---|---|
| `Read`, `Glob`, `Grep`, `Write`, `Edit`, `Bash` | Use the host's file, search, edit and shell tools. Bash examples require Bash even when the host shell is PowerShell. |
| `AskUserQuestion` | Use the host's question tool or ask in chat and wait when an answer is required. |
| `Skill` or `/name` | Load `python scripts/studio.py skill name`; preserve the supplied arguments. |
| `Agent` / `Task`, named `subagent_type` | Read `python scripts/studio.py agent <role>`. Delegate with that role's instructions if the host supports it. Otherwise perform the roles sequentially, explicitly labelled; independent review remains unassessed. |
| `TaskCreate`, `TaskGet`, `TaskList`, `TaskUpdate` | Use the host's task list, or a labelled checklist in the session checkpoint. |
| `model: opus/sonnet/haiku`, `maxTurns`, `memory`, `allowed-tools` | Claude metadata, not cross-provider settings or permission grants. Use the selected host model and actual available capabilities. |
| `@path` imports in Claude instructions | Read the referenced document explicitly when relevant; do not assume automatic expansion. |

`team.size` and review modes retain their meaning. A sequential role pass is
available on a minimal harness such as pi without requiring a subagent extension,
but it is not equivalent to isolated or parallel agents. If a workflow requires
independence, report that gate as unassessed until an independent review exists.

### Configuration, rules and hooks

Python **3.9+** runs the renderer using only the standard library. Use `python3`
or `py -3` in place of `python` if needed. Existing helpers also require Bash;
on Windows use Git Bash (a WSL `bash.exe` may not have the same paths or tools).

For example, run this in Bash from the root:

```bash
bash .claude/hooks/yaml-helper.sh resolve_config --keys review_mode,automation,workflow,team.size
```

Keep the existing resolver and its local override/rigor/legacy precedence. If
Bash or Python is unavailable, stop dependent workflow steps and name the missing
runtime; do not claim settings were resolved. Before editing, read matching
`.claude/rules/*.md` rules explicitly as directed by `AGENTS.md`.

This adapter does **not** register hooks, permissions, a status line, desktop
notifications, agent audit events, or session lifecycle handlers with other
CLIs. It also does not disable compatibility features that a CLI already has.
Some clients import Claude configuration themselves; inspect their effective
settings before relying on them. `.claude/settings.json` is not a portable
security policy. Use the host's permission controls. Checkpointing, rule
application and validation are agent-driven in portable mode, not enforced by
this adapter. Do not invoke an event hook with empty input and report that it
validated a commit or file; those hooks expect Claude event payloads.

## Verification and maintenance

```bash
python scripts/studio.py list
python scripts/studio.py skill help
python -m unittest discover -s scripts/tests -v
```

Tests cover rendering all workflows, roles and supporting documents, directory
containment, explicit-only instructions, no implicit command execution, and
running from a different directory with spaces and Unicode in the repo path.
They do not test model judgment or authenticated end-to-end game development in
all five clients. Muse Code availability and client trust/settings are separate
from the adapter tests. Restart/reload a client's skills after pulling changes.

Verified locally on Windows (2026-10-18): all 8 adapter regression tests passed
over 74 workflows, 117 supporting documents and 49 roles; the existing resolver
ran successfully in Git Bash. pi 1.2.0's offline RPC `get_commands` discovered
`skill:studio` from this project's `.agents/skills/studio/SKILL.md`, with no model
request. Codex 0.162.1, Antigravity 1.3.4 and Grok 1.0.44 were present, but their
model-driven workflow execution was not tested. Muse Code was not on PATH.

Edit original workflows under `.claude/skills/`; the adapter reads changes on
the next invocation. Keep this file and `AGENTS.md` aligned with upstream studio
conventions when upgrading. The two small `studio` entrypoints share one runtime
contract, and no generated workflow copies need refreshing.

Official discovery references (checked 2026-10-18):

- [Codex skills](https://developers.openai.com/codex/skills)
- [Antigravity CLI skills](https://antigravity.google/docs/skills?app=cli) and [rules](https://antigravity.google/docs/rules/)
- [Muse Code skills](https://meta-models.github.io/muse-code-sdk/next/guides/extend/skills/)
- [Grok Build skills and project instructions](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-shell/README.md)
- [pi skills](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/skills.md)
