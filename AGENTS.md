# Company of Gamers — local CLI instructions

This is a game studio template with 49 role prompts and 74 workflows. Its
canonical content remains under `.claude/` for upstream and Claude Code
compatibility; those files do not require a Claude model.

## Start here

- Work from the repository root (the directory containing `project.yaml`).
- Read `docs/local-cli.md` before using studio workflows outside Claude Code.
- Read `.claude/docs/coding-standards.md` and
  `.claude/docs/coordination-rules.md`. Apply the tool/capability translations
  in `docs/local-cli.md` to Claude-specific instructions in those documents.
- Read `production/session-state/active.md` if it exists when starting or
  resuming work. Keep it current before finishing; do not rely on automatic
  session or compaction hooks in portable mode.
- Read `project.yaml` and, if present, `project.local.yaml`. Resolve settings
  using `.claude/hooks/yaml-helper.sh` as described in `docs/local-cli.md`.
  Do not pin the six rigor-fronted knobs when onboarding a new project.
- Before editing, inspect `.claude/rules/*.md` frontmatter and read every rule
  whose `paths` cover the files being changed. Rules are instructions to apply
  manually here, not automatically installed enforcement.
- Read `.claude/docs/directory-structure.md` for layout and the chosen engine's
  `docs/engine-reference/<engine>/VERSION.md` on demand. Do not assume Godot.

## Workflows

Use the `studio` skill with a workflow name, for example `studio start` or
`studio team-combat melee parry`. Run `python scripts/studio.py list` for names.
Load workflows with `python scripts/studio.py skill <name>` and follow the
rendered instructions. This command only prints instructions; the CLI agent
performs the work. Pass the user's remaining text as workflow arguments in
conversation, never by evaluating it in a shell.

For Claude Code, `CLAUDE.md` and the original `/start`, `/team-combat`, etc.
remain the native entrypoints. Other CLIs should use the portable `studio`
entrypoint even if they also discover the original Claude skills.

## Collaboration and evidence

Respect the user's authorized scope and `modes.automation`; for new decisions
outside that scope, present the options and obtain the required answer before
proceeding. Never treat a dismissed question as approval. No commits or pushes
without user instruction. The host CLI's permissions remain authoritative.

Use available delegation tools for role prompts, or disclose sequential role
execution when delegation is unavailable. Never call a self-review an independent
review. Mark unavailable mandatory checks `NOT ASSESSED` or `BLOCKED`, not passed.
Player-visible game changes require a real run and retained screenshots in
`production/qa/evidence/`; a parse check is not a run.
