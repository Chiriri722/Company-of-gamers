#!/usr/bin/env python3
"""Render existing studio workflows for local CLI agents; never execute them."""

import argparse
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
INJECTION = re.compile(r"^!`([^\n]+)`[ \t]*$", re.MULTILINE)


def read_document(path):
    """Split optional frontmatter from UTF-8 Markdown without a YAML dependency."""
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---\n"):
        return "", text
    header, separator, body = text[4:].partition("\n---\n")
    if not separator:
        raise ValueError(f"Unterminated frontmatter: {path.relative_to(ROOT)}")
    return header, body.lstrip("\n")


def source_path(kind, name, reference=None):
    """Resolve only known role/workflow names and contained Markdown references."""
    if not NAME.fullmatch(name):
        raise ValueError("Use a catalog name containing lowercase letters, digits and hyphens.")
    base = ROOT / ".claude" / ("agents" if kind == "agent" else "skills")
    folder = base if kind == "agent" else base / name
    path = folder / (f"{name}.md" if kind == "agent" else "SKILL.md")
    if reference is not None:
        path = folder / reference
    resolved = path.resolve()
    # Also reject symlinks that escape the canonical content directory.
    if not resolved.is_relative_to(folder.resolve()) or not resolved.is_relative_to(base.resolve()):
        raise ValueError("Reference must stay inside the selected skill directory.")
    if resolved.suffix != ".md" or not resolved.is_file():
        raise ValueError(f"Unknown {kind} or Markdown reference. Run: python scripts/studio.py list")
    return resolved


def render(kind, name, reference=None):
    path = source_path(kind, name, reference)
    header, body = read_document(path)
    source_dir = f".claude/skills/{name}"
    body = re.sub(r"\$\{CLAUDE_SKILL_DIR\}|\$CLAUDE_SKILL_DIR\b", source_dir, body)
    body = re.sub(r"\$\{CLAUDE_PROJECT_DIR\}|\$CLAUDE_PROJECT_DIR\b", ".", body)

    def explicit_step(match):
        return (
            "**Context step — run this in Bash from the repository root before "
            "using its output below (it has NOT run yet):**\n\n"
            f"```bash\n{match.group(1)}\n```\n\n"
            "If unavailable or unsuccessful, report NOT ASSESSED and stop any "
            "dependent decision; do not silently use default settings."
        )

    body = INJECTION.sub(explicit_step, body)
    explicit_only = bool(re.search(r"^disable-model-invocation:\s*true\s*$", header, re.MULTILINE))
    preface = (
        f"# Portable studio {kind}: {name}\n\n"
        f"Source: `{path.relative_to(ROOT).as_posix()}`\n\n"
        "Read `AGENTS.md` and `docs/local-cli.md` before following this content. "
        "Use the current CLI's tools and model, not Claude-only metadata. "
        "Commands run from the repository root. `$ARGUMENTS` means the user's "
        "remaining workflow text, kept as data, never shell interpolation. "
        "Any statement below that context was already resolved applies only "
        "AFTER you actually run the corresponding context step successfully.\n\n"
    )
    if kind != "agent":
        preface += (
            f"Relative skill resources such as `references/` resolve under `{source_dir}/`, "
            "not under the portable entrypoint. Load them with "
            f"`python scripts/studio.py reference {name} <relative-path>`.\n\n"
        )
    if explicit_only:
        preface += "**Explicit invocation required:** run this workflow only when the user requested it.\n\n"
    return preface + body


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List available workflows and roles")
    for kind in ("skill", "agent", "reference"):
        command = commands.add_parser(kind, help=f"Print a portable {kind} prompt")
        command.add_argument("name")
        if kind == "reference":
            command.add_argument("path", help="Markdown path relative to the canonical skill directory")
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            for label, pattern in (("Workflows", "skills/*/SKILL.md"), ("Roles", "agents/*.md")):
                paths = sorted((ROOT / ".claude").glob(pattern))
                print(f"{label} ({len(paths)}):")
                for path in paths:
                    print(f"  {path.parent.name if label == 'Workflows' else path.stem}")
        else:
            print(render(args.command, args.name, getattr(args, "path", None)))
    except (OSError, ValueError) as error:
        print(f"studio: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    # Windows pipes may otherwise choose a legacy codepage for Unicode prompts.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
