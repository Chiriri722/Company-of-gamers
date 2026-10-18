---
name: studio
description: Run Company of Gamers game development workflows for onboarding, design, architecture, implementation, reviews, QA, and team coordination. Use with a workflow name such as start, brainstorm, dev-story, or team-combat.
---

# Company of Gamers

1. Locate the repository root containing `project.yaml` and `scripts/studio.py`
   (three directories above this skill). Run commands from that root.
2. Read `AGENTS.md` and `docs/local-cli.md` there, even if the host did not load
   project instructions automatically.
3. Treat the first user argument as a workflow name; the remaining text is its
   arguments. Without a name, use `help`; with `list`, print the workflow catalog.
   Run `python scripts/studio.py list` to discover names when needed.
4. Load `python scripts/studio.py skill <name>`, then follow its entire output.
   The renderer only prints instructions. Explicit shell steps still need to
   run through the host's tools and permissions. Do not interpolate workflow
   arguments into shell commands. Keep paths containing spaces as one value.
5. Load supporting documents with
   `python scripts/studio.py reference <name> references/<file>.md` when requested
   by the workflow. Load role prompts with `python scripts/studio.py agent <name>`.
6. Translate workflow handoffs such as `/setup-engine godot 4.6` into another
   `studio` workflow invocation, preserving arguments. Apply the capability
   fallbacks in `docs/local-cli.md`; report unavailable checks explicitly.

Use `python3` or `py -3` if that is how Python 3 is installed. If output is
truncated, read the remaining source sections before proceeding; never execute
a workflow from an incomplete prompt.
