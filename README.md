<p align="center">
  <h1 align="center">Company of Gamers</h1>
  <p align="center">
    Turn a local coding-agent session into a coordinated game development studio.
    <br />
    49 agents. 74 skills. One coordinated AI team.
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href=".claude/agents"><img src="https://img.shields.io/badge/agents-49-blueviolet" alt="49 Agents"></a>
  <a href=".claude/skills"><img src="https://img.shields.io/badge/skills-74-green" alt="74 Skills"></a>
  <a href=".claude/hooks"><img src="https://img.shields.io/badge/hooks-12-orange" alt="12 Hooks"></a>
  <a href=".claude/rules"><img src="https://img.shields.io/badge/rules-13-red" alt="13 Rules"></a>
  <a href="#local-cli-support"><img src="https://img.shields.io/badge/local%20CLI-Codex%20%7C%20Antigravity%20%7C%20Muse%20%7C%20Grok%20%7C%20pi-blue" alt="Local CLI support"></a>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20this%20project-FFDD00?logo=buymeacoffee&logoColor=black" alt="Buy Me a Coffee"></a>
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/GitHub%20Sponsors-Support%20this%20project-ea4aaa?logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

---

## Why This Exists

Building a game solo with AI is powerful — but a single chat session has no structure. No one stops you from hardcoding magic numbers, skipping design docs, or writing spaghetti code. There's no QA pass, no design review, no one asking "does this actually fit the game's vision?"

**Company of Gamers**, based on [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios), gives your AI session the structure of a real studio. Its 49 role prompts form a studio hierarchy — directors who guard the vision, department leads who own their domains, and specialists who do the hands-on work. Each role has defined responsibilities, escalation paths, and quality gates. Claude Code uses native subagents; other local CLIs use the portable `studio` entrypoint with the delegation capabilities available in that host.

The result: you still make every decision, but now you have a team that asks the right questions, catches mistakes early, and keeps your project organized from first brainstorm to launch.

---

## Table of Contents

- [What's Included](#whats-included)
- [Studio Hierarchy](#studio-hierarchy)
- [Slash Commands](#slash-commands)
- [Does it produce games, or documents?](#does-it-produce-games-or-documents)
- [Getting Started](#getting-started)
- [Local CLI Support](#local-cli-support)
- [Configuration](#configuration)
- [Upgrading](#upgrading)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Design Philosophy](#design-philosophy)
- [Customization](#customization)
- [Platform Support](#platform-support)
- [Community](#community)
- [Supporting This Project](#supporting-this-project)
- [License](#license)

---

## What's Included

| Category | Count | Description |
|----------|-------|-------------|
| **Agents** | 49 | Role prompts across design, programming, art, audio, narrative, QA, and production; native subagents in Claude Code |
| **Skills** | 74 | Workflows for every phase; original slash commands in Claude Code, routed through `studio` on other CLIs |
| **Hooks** | 12 | Claude Code event integrations for validation, session lifecycle, agent audit trail, and gap detection |
| **Rules** | 13 | Path-scoped standards; automatically loaded by Claude Code, explicitly read and applied in portable mode |
| **Templates** | 39 | Document templates for GDDs, UX specs, ADRs, sprint plans, HUD design, accessibility, and more |

## Studio Hierarchy

Agents are organized into three tiers, matching how real studios operate:

```
Tier 1 — Directors
  creative-director    technical-director    producer

Tier 2 — Department Leads
  game-designer        lead-programmer       art-director
  audio-director       narrative-director    qa-lead
  release-manager      localization-lead

Tier 3 — Specialists
  gameplay-programmer  engine-programmer     ai-programmer
  network-programmer   tools-programmer      ui-programmer
  systems-designer     level-designer        economy-designer
  technical-artist     sound-designer        writer
  world-builder        ux-designer           prototyper
  performance-analyst  devops-engineer       analytics-engineer
  security-engineer    qa-tester             accessibility-specialist
  live-ops-designer    community-manager
```

In Claude Code, agent frontmatter selects models: the three directors ask for
Opus, `lead-programmer` and fifteen specialists name Sonnet, and the remaining thirty
**inherit your session's model**. Treat the tiers as seniority of role, not as
a billing plan — most of the studio runs on whatever model you are already using.
Portable mode uses your host CLI's selected model; Anthropic model names are not
translated into other providers' model IDs.

### Engine Specialists

The template includes agent sets for all three major engines. Use the set that matches your project:

| Engine | Lead Agent | Sub-Specialists |
|--------|-----------|-----------------|
| **Godot 4** | `godot-specialist` | GDScript, Shaders, GDExtension |
| **Unity** | `unity-specialist` | DOTS/ECS, Shaders/VFX, Addressables, UI Toolkit |
| **Unreal Engine 5** | `unreal-specialist` | GAS, Blueprints, Replication, UMG/CommonUI |

## Slash Commands

Type `/` in Claude Code to access all 74 skills. On other CLIs, use the shared
`studio` skill followed by the workflow name and arguments: `$studio brainstorm`
in Codex, `/studio brainstorm` in Antigravity/Grok, or `/skill:studio brainstorm`
in pi. In Muse Code, select `studio` from `/skills` and request `brainstorm`.
The `/name` notation below names the original workflow; it does not mean every
host registers that name as a separate command.

**Onboarding & Navigation**
`/start` `/help` `/project-stage-detect` `/setup-engine` `/adopt` `/settings`

**Game Design**
`/brainstorm` `/map-systems` `/design-system` `/quick-design` `/review-all-gdds` `/propagate-design-change`

**Art & Assets**
`/art-bible` `/asset-spec` `/asset-audit`

**UX & Interface Design**
`/ux-design` `/ux-review`

**Architecture**
`/create-architecture` `/architecture-decision` `/architecture-review` `/create-control-manifest`

**Stories & Sprints**
`/create-epics` `/create-stories` `/dev-story` `/sprint-plan` `/sprint-status` `/story-readiness` `/story-done` `/estimate`

**Reviews & Analysis**
`/design-review` `/code-review` `/balance-check` `/content-audit` `/scope-check` `/perf-profile` `/tech-debt` `/gate-check` `/consistency-check` `/security-audit`

**QA & Testing**
`/qa-plan` `/smoke-check` `/soak-test` `/regression-suite` `/test-setup` `/test-helpers` `/test-evidence-review` `/test-flakiness` `/skill-test` `/skill-improve`

**Production**
`/milestone-review` `/retrospective` `/bug-report` `/bug-triage` `/reverse-document` `/playtest-report`

**Release**
`/release-checklist` `/launch-checklist` `/changelog` `/patch-notes` `/hotfix` `/day-one-patch`

**Creative & Content**
`/prototype` `/vertical-slice` `/onboard` `/localize`

**Team Orchestration** (coordinate multiple agents on a single feature)
`/team-combat` `/team-narrative` `/team-ui` `/team-release` `/team-polish` `/team-audio` `/team-level` `/team-live-ops` `/team-qa`

## Does it produce games, or documents?

A fair question, and the answer is a measurement rather than a sample project.
Four games were built from one brief at different `modes.rigor` levels and the
documents each wrote **before its first line of game code** were counted:

| `modes.rigor` | Docs before first line of game code | Time |
|---|---:|---:|
| `minimal` | **1** (the one-page brief) | 0 min |
| `standard` | 30 | 58 min |

All of them produced a running, tested game. Two blind reviewers and a human
playtest then ranked the `standard` build **last** — the extra 29 documents
bought traceability, not a better game.

### It runs the game and looks at it

The measurement above is about cost. The other half is whether the thing works,
and for a game that means someone has to *look* at it — a passing test says
nothing about a menu drawn off-screen. So a story that changes anything the
player sees is not closed until the game has been launched, observed, and a
screenshot retained in `production/qa/evidence/`. A parse check is not a run.
This holds at every rigor level, including `minimal`, where automated tests are
waived but the look is not.

The games themselves are deliberately **not** shipped here: this is a template
you clone to start your own project, and somebody else's game in your repo is
clutter, not evidence.

## Getting Started

### Prerequisites

- [Git](https://git-scm.com/)
- An installed, authenticated **Codex CLI, Antigravity CLI, Muse Code, Grok Build, pi**, or [Claude Code](https://code.claude.com/docs/en/setup)
- [Python 3.9+](https://www.python.org/) — runs the portable prompt renderer and existing configuration helpers; no extra Python packages required
- Bash — runs configuration helpers and existing hooks; on Windows use the Bash included with [Git for Windows](https://git-scm.com/downloads/win)
- **Recommended**: [jq](https://jqlang.github.io/jq/) (for hook validation)

In Claude Code, hooks generally degrade when optional tools are missing, except
that a commit staging data JSON is blocked without Python validation. Portable
mode does not install those event hooks; missing runtimes or mandatory checks
must be reported rather than silently treated as successful validation.

### Setup

1. **Clone or use as template**:
   ```bash
   git clone https://github.com/Chiriri722/Company-of-gamers.git my-game
   cd my-game
   ```

2. **Check the portable workflow catalog** from the root (the folder holding
   `AGENTS.md` and `project.yaml`):
   ```bash
   python scripts/studio.py list
   ```
   Use `python3` or `py -3` if needed. This only lists prompts; it does not start
   a model session or run a game workflow.

3. **Launch your CLI at that root and invoke `studio start`** using the syntax
   in the table below. The system asks where you are (no idea, vague concept,
   clear design, existing work) and guides you to the right workflow. No assumptions.

   Or jump directly to a specific skill if you already know what you need:
   - `studio brainstorm` — explore game ideas from scratch
   - `studio setup-engine godot 4.6` — configure your engine if you already know
   - `studio project-stage-detect` — analyze an existing project

For **Claude Code**, launch `claude` at the same root and use the original
`/start`, `/brainstorm`, etc. Its `CLAUDE.md`, settings, hooks and skills remain
unchanged. Starting Claude Code in a subfolder can skip root hooks and settings.

## Local CLI Support

First-wave support is a **portable prompt/workflow adapter**, not full native
hook or subagent parity. One shared `studio` skill loads the 74 original
workflows and 49 role prompts on demand.

| CLI | Launch | Start inside the session | Discovery |
|---|---|---|---|
| Codex | `codex` | `$studio start` | `.agents/skills/studio/` |
| Antigravity | `agy` | `/studio start` | `.agents/skills/studio/` |
| Muse Code | `muse` | `/skills` → select `studio`, then request `start` | `.agents/skills/studio/` |
| Grok Build | `grok` | `/studio start`, or `/skills studio` then request `start` | `.grok/skills/studio/` |
| pi | `pi` | `/skill:studio start` | `.agents/skills/studio/` |

If skill discovery is unavailable, ask: **Read
`.agents/skills/studio/SKILL.md` and run the `start` workflow.** Accept project
trust through the host's normal flow; Muse Code skips project skills in an
untrusted workspace. Keep using `studio` on clients that also discover Claude
skills so the portable conversion is applied.

The adapter removes Claude-specific frontmatter, replaces directory variables,
and turns shell preprocessing into explicit command steps. It keeps existing
configuration, workflow content, templates and supporting references in place.
Use native delegation when available; otherwise disclose sequential role passes.
An independent-review requirement cannot be satisfied by relabelling self-review.

**Not ported:** automatic lifecycle/validation hooks, permission rules, model
pins, status line, notifications, and native registration of 49 subagents.
Apply path rules and maintain session checkpoints explicitly. Tests cover the
adapter and every source prompt; authenticated end-to-end sessions across all
five clients are not yet verified. pi 1.2.0's offline command discovery was also
verified locally. For the runtime contract, verification
commands and official discovery references, see [Local CLI compatibility](docs/local-cli.md).

## Configuration

`project.yaml` at the repo root is the single source of truth for how the
studio behaves on your project — engine, naming conventions, and a `modes`
block that controls how much process every skill enforces. `/start` writes it
for you; you rarely need to hand-edit it.

The one question that matters most is **`modes.rigor`** — `minimal`, `standard`,
or `full`. It's a single front door over six separate knobs (`workflow` —
which GDD sections are required, `docs.density`, `qa.level`,
`story_granularity`, `review_mode` — how many director agents review your work,
and `team.size`), so `/start` asks it once instead of six times:

- **`minimal`** (default) — jam-game speed. No GDDs required, terse docs, minimal QA evidence, solo review. `/start` → `/setup-engine` → `/brainstorm` (a one-page brief) → `/create-stories` → `/dev-story` ↔ `/story-done`.
- **`standard`** — 5 required GDD sections, balanced doc depth, standard QA evidence, lean review.
- **`full`** — all 8 GDD sections, thorough docs, full QA evidence on every story type, full director review.

`minimal` is the default because the heavier tier costs more to reach working
code without producing a better result, and gives nothing back when someone new
picks the project up. Raise it in one `/settings` call when your project grows
— `/help` and `/gate-check` will suggest it when they see the signs.

Two escape hatches keep one setting from being a blunt instrument.
**`system_overrides`** holds a single system to a higher standard than the rest
of the project — your combat system gets the full treatment while everything
else stays light. **`testing.strict`** sets, per test type (logic, integration,
visual, UI, config), whether missing evidence blocks a story or merely warns.

Any of the six underlying knobs can still be set individually if you want a mix
(e.g. `workflow: full` with `docs.density: terse` — comprehensive but compact).
Two of them — `review_mode` (`full` / `lean` / `solo`) and `team.size` — are
also **personal**: rigor sets the team-wide default, but you can override them
per-developer in a gitignored `project.local.yaml` without touching the shared
config. `modes.automation` (how often the AI pauses to ask before it acts) sits
outside rigor and is likewise personally overridable.

View or change any setting with the `/settings` skill:

```
/settings                              # view effective config
/settings modes.review_mode            # view one setting
/settings modes.rigor=full             # write to project.yaml (team-wide)
/settings --local modes.review_mode=solo   # write to project.local.yaml (just you)
```

Full schema and per-setting behavior: `.claude/docs/effects-map.md`.

## Upgrading

Already using an older version of this template? See [UPGRADING.md](UPGRADING.md)
for step-by-step migration instructions, a breakdown of what changed between
versions, and which files are safe to overwrite vs. which need a manual merge.
Preserve this fork's `AGENTS.md`, `docs/local-cli.md`, `scripts/studio.py` and
the two `studio` entrypoints when applying upstream updates. Original skills
remain under `.claude/`; the adapter reads their latest content on demand.

## Project Structure

```
AGENTS.md                           # Portable project instructions
CLAUDE.md                           # Claude Code project instructions
project.yaml                        # Shared project configuration
.agents/skills/studio/SKILL.md       # Codex, Antigravity, Muse Code, pi entrypoint
.grok/skills/studio/SKILL.md         # Grok Build entrypoint, delegates to shared skill
scripts/studio.py                   # Read-only portable prompt renderer
scripts/tests/                      # Adapter regression tests
docs/local-cli.md                   # Compatibility contract and client instructions
.claude/
  settings.json                     # Hooks, permissions, safety rules
  agents/                           # 49 agent definitions (markdown + YAML frontmatter)
  skills/                           # 74 slash commands (subdirectory per skill)
  hooks/                            # 14 scripts (bash) — 12 event hooks, yaml-helper.sh,
                                    #   and one opt-in diagnostic you wire yourself
  rules/                            # 13 path-scoped coding standards
  statusline.sh                     # Status line script (context%, model, stage, epic breadcrumb)
  docs/
    workflow-catalog.yaml           # 7-phase pipeline definition (read by /help)
    templates/                      # 39 document templates (+ per-section guidance)
src/                                # Game source code (Godot). The code root is
                                    #   ENGINE-SPECIFIC: Unity compiles only
                                    #   Assets/, Unreal builds from Source/<Module>/
assets/                             # Art, audio, VFX, shaders, data files
design/                             # GDDs, narrative docs, level designs
docs/                               # Technical documentation and ADRs
tests/                              # Test suites (unit, integration, performance, playtest)
tools/                              # Build and pipeline tools
prototypes/                         # Throwaway prototypes (isolated from src/)
production/                         # Sprint plans, milestones, release tracking
CCGS Skill Testing Framework/       # QA for the skills and agents themselves — see below
```

### Testing your customizations

CCGS is a template you are meant to edit. `CCGS Skill Testing Framework/` is how
you check that an edited or newly written skill still holds up — a catalog of all
74 skills and 49 agents, per-category quality rubrics, behavioral specs, and
templates for writing specs of your own.

```
/skill-test static [name]     # structural linter — 7 compliance checks
/skill-test category [name]   # category-specific quality rubric
/skill-test spec [name]       # behavioral spec assertions
/skill-test audit             # coverage report across skills and agents
/skill-improve [name]         # test-fix-retest loop; keeps or reverts on score change
```

It tests the *framework*, never your game — game tests live in `tests/`.
On portable clients, invoke these through `studio`, for example
`studio skill-test static start`. Run the adapter's automated regression suite
separately with `python -m unittest discover -s scripts/tests -v`.

## How It Works

### Agent Coordination

Agents follow a structured delegation model:

1. **Vertical delegation** — directors delegate to leads, leads delegate to specialists
2. **Horizontal consultation** — same-tier agents can consult each other but can't make binding cross-domain decisions
3. **Conflict resolution** — disagreements escalate up to the shared parent (`creative-director` for design, `technical-director` for technical)
4. **Change propagation** — cross-department changes are coordinated by `producer`
5. **Domain boundaries** — agents don't modify files outside their domain without explicit delegation

### Collaboration Modes

By default, `modes.automation: collaborative` follows this collaboration protocol:

1. **Ask** — agents ask questions before proposing solutions
2. **Present options** — agents show 2-4 options with pros/cons
3. **You decide** — the user always makes the call
4. **Draft** — agents show work before finalizing
5. **Approve** — nothing gets written without your sign-off

You stay in control. The agents provide structure and expertise, not autonomy.

The `guided` and `autonomous` workflow settings trade some prompts for speed.
Portable sessions respect the user's already authorized scope and the host's
permission controls. Claude Code also has its own auto mode; see
[setup-requirements.md](.claude/docs/setup-requirements.md) for the routes into
auto mode.

### Automated Safety

In **Claude Code**, these hooks are registered by the project settings. The
portable adapter does not register them with other CLIs:

| Hook | Trigger | What It Does |
|------|---------|--------------|
| `validate-commit.sh` | PreToolUse (Bash, PowerShell) | Checks for hardcoded values, TODO format, JSON validity, design doc sections — exits early if the command is not `git commit` |
| `validate-push.sh` | PreToolUse (Bash, PowerShell) | Warns on pushes to protected branches — exits early if the command is not `git push` |
| `validate-assets.sh` | PostToolUse (Write/Edit) | Checks data-file JSON under `assets/`, `Assets/` or `Content/`, and asset naming in Godot's `assets/` only — exits early if the file is under none of them |
| `session-start.sh` | Session open | Shows current branch and recent commits for orientation |
| `detect-gaps.sh` | Session open | Detects fresh projects (suggests `/start`) and missing design docs when code or prototypes exist |
| `pre-compact.sh` | Before compaction | Logs the compaction (its output does not reach Claude — `session-start.sh` restores context afterwards) |
| `post-compact.sh` | After compaction | Debug-log reminder only (its output does not reach Claude) |
| `notify.sh` | Notification event | Shows Windows toast notification via PowerShell |
| `session-stop.sh` | Every response end | Archives `active.md` to session log and records git activity |
| `log-agent.sh` | Agent spawned | Audit trail start — logs subagent invocation |
| `log-agent-stop.sh` | Agent stops | Audit trail stop — completes subagent record |
| `validate-skill-change.sh` | PostToolUse (Write/Edit) | Advises running `/skill-test` after any `.claude/skills/` change |

> **Note**: `validate-commit.sh`, `validate-assets.sh`, and `validate-skill-change.sh` fire on every Bash, PowerShell or Write tool call and exit immediately (exit 0) when the command or file path is not relevant. This is normal hook behavior — not a performance concern.

**Permission rules** in `settings.json` auto-allow test runs and block dangerous operations (force push, `rm -rf`, reading `.env` files) in both the Bash and PowerShell tools. Read-only commands such as `git status`, `git log` and `ls` need no rule: Claude Code runs them without asking. The `git` rules match anywhere after `git`, so a git command whose text only mentions `push` followed later by ` +` or ` -f`, `clean` followed by ` -f`, or `reset` followed by `--hard` — a commit message such as `git commit -m "push + pull"` included — is denied too: reword the message.

### Path-Scoped Rules

Claude Code automatically loads coding standards based on file location.
In portable mode, `AGENTS.md` directs the agent to read and apply matching rules;
this is instruction-based behavior rather than automatic enforcement. The paths
below are Godot's. Each rule also matches the Unity and Unreal layouts: the code
rules match C# under `Assets/**/Gameplay/` and C++ under `Source/**/Gameplay/` (and `Core`,
`AI`, `Networking`, `UI`), data matches JSON under `Assets/**/Data/` and
`Content/**/Data/`, shaders match by file type, and tests match
C# under `Assets/Tests/` and C++ under `Source/**/Tests/`.

| Path | Enforces |
|------|----------|
| `src/gameplay/**` | Data-driven values, delta time usage, no UI references |
| `src/core/**` | Zero allocations in hot paths, thread safety, API stability |
| `src/ai/**` | Performance budgets, debuggability, data-driven parameters |
| `src/networking/**` | Server-authoritative, versioned messages, security |
| `src/ui/**` | No game state ownership, localization-ready, accessibility |
| `design/gdd/**` | Required sections per `modes.workflow`, formula format, edge cases |
| `design/narrative/**` | Lore consistency, character voice, canon levels |
| `assets/data/**/*.json` | JSON validity, naming conventions, schema rules |
| `assets/shaders/**` | Naming conventions, performance targets, cross-platform rules |
| `tests/**` | Test naming, coverage requirements, fixture patterns |
| `prototypes/**` | Relaxed standards, README required, hypothesis documented |

## Design Philosophy

This template is grounded in professional game development practices:

- **MDA Framework** — Mechanics, Dynamics, Aesthetics analysis for game design
- **Self-Determination Theory** — Autonomy, Competence, Relatedness for player motivation
- **Flow State Design** — Challenge-skill balance for player engagement
- **Bartle Player Types** — Audience targeting and validation
- **Verification-Driven Development** — Tests first, then implementation

## Customization

This is a **template**, not a locked framework. Everything is meant to be customized:

- **Add/remove agents** — delete agent files you don't need, add new ones for your domains
- **Edit agent prompts** — tune agent behavior, add project-specific knowledge
- **Modify skills** — adjust workflows to match your team's process
- **Add rules** — create new path-scoped rules for your project's directory structure
- **Tune hooks** — adjust validation strictness, add new checks
- **Pick your engine** — use the Godot, Unity, or Unreal agent set (or none)
- **Tune process weight** — `modes.rigor` and its underlying knobs in `project.yaml` (see [Configuration](#configuration)). Override per-run with `--review solo` on any skill.

## Platform Support

The portable renderer uses standard-library Python 3.9+ and is tested on Windows,
including paths with spaces and Unicode. Configuration helpers were exercised
with Git Bash. macOS/Linux adapter runs and authenticated workflow sessions in
all five CLIs still need validation; support here describes the implemented
entrypoints and prompt adaptation, not a completed client/OS certification matrix.

The upstream project reports hook/script coverage on Windows with Git Bash,
macOS bash 3.2/BSD tools, and Linux. `notify.sh` provides Windows notifications
only. These Claude event hooks are separate from portable CLI support.

## Community

- **Discussions** — [GitHub Discussions](https://github.com/Donchitos/Claude-Code-Game-Studios/discussions) for questions, ideas, and showcasing what you've built
- **Issues** — [Company of Gamers bugs and feature requests](https://github.com/Chiriri722/Company-of-gamers/issues)

---

## Supporting This Project

Company of Gamers builds on the free and open-source Claude Code Game Studios.
The links below support the upstream creator, Donchitos:

<p>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee"></a>
  &nbsp;
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/GitHub%20Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

- **[Buy Me a Coffee](https://www.buymeacoffee.com/donchitos3)** — one-time support
- **[GitHub Sponsors](https://github.com/sponsors/Donchitos)** — recurring support through GitHub

Sponsorships help fund time spent maintaining skills, adding new agents, keeping up with Claude Code and engine API changes, and responding to community issues.

---

*Originally built for Claude Code; extended with portable workflows for Codex,
Antigravity, Muse Code, Grok Build and pi.*

## License

MIT License. See [LICENSE](LICENSE) for details.
