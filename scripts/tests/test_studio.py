"""Portable adapter tests; no model requests, credentials, or game writes."""

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("studio", ROOT / "scripts/studio.py")
studio = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(studio)


class StudioTests(unittest.TestCase):
    def test_all_workflows_and_references_render(self):
        manifests = list((ROOT / ".claude/skills").glob("*/SKILL.md"))
        self.assertTrue(manifests)
        for manifest in manifests:
            for path in manifest.parent.rglob("*.md"):
                with self.subTest(path=path.relative_to(ROOT)):
                    kind = "skill" if path == manifest else "reference"
                    reference = None if kind == "skill" else str(path.relative_to(manifest.parent))
                    output = studio.render(kind, manifest.parent.name, reference)
                    header, body = studio.read_document(path)
                    self.assertNotIn("CLAUDE_SKILL_DIR", output)
                    self.assertNotIn("CLAUDE_PROJECT_DIR", output)
                    self.assertIsNone(studio.INJECTION.search(output))
                    self.assertEqual(output.count("**Context step —"), len(studio.INJECTION.findall(body)))
                    if "disable-model-invocation: true" in header:
                        self.assertIn("Explicit invocation required", output)
                    self.assertIn(f".claude/skills/{manifest.parent.name}/", output)

    def test_all_roles_render_without_claude_frontmatter(self):
        roles = list((ROOT / ".claude/agents").glob("*.md"))
        self.assertTrue(roles)
        for role in roles:
            with self.subTest(role=role.stem):
                output = studio.render("agent", role.stem)
                self.assertIn(studio.read_document(role)[1], output)
                self.assertNotRegex(output, r"(?m)^model:")

    def test_paths_point_to_original_helpers_and_references(self):
        output = studio.render("skill", "team-combat")
        self.assertIn('bash ".claude/skills/team-combat/../../hooks/yaml-helper.sh"', output)
        self.assertIn("NOT ASSESSED", output)
        output = studio.render("reference", "create-architecture", "references/1-layers.md")
        self.assertIn(".claude/skills/create-architecture/references/1-layers.md", output)

    def test_rejects_unknown_names_and_reference_escape(self):
        for name in ("../start", "start;echo", "not-a-real-workflow"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                studio.render("skill", name)
        for path in ("../start/SKILL.md", "../../../settings.json", str(ROOT / "README.md")):
            with self.subTest(path=path), self.assertRaises(ValueError):
                studio.render("reference", "help", path)

    def test_cli_reports_error_and_lists_actual_catalog(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/studio.py"), "skill", "unknown"],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unknown", result.stderr)
        self.assertEqual(result.stdout, "")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/studio.py"), "list"],
                                capture_output=True, text=True, encoding="utf-8", check=True)
        for path in (ROOT / ".claude/skills").glob("*/SKILL.md"):
            self.assertIn(f"  {path.parent.name}\n", result.stdout)

    def test_other_cwd_unicode_paths_and_no_implicit_execution(self):
        with tempfile.TemporaryDirectory(prefix="studio test ") as tmp:
            root = Path(tmp) / "게임 project"
            (root / "scripts").mkdir(parents=True)
            source = root / ".claude/skills/probe"
            source.mkdir(parents=True)
            shutil.copy2(ROOT / "scripts/studio.py", root / "scripts/studio.py")
            (source / "SKILL.md").write_text(
                '---\nname: probe\ndescription: test\nmodel: opus\n'
                'disable-model-invocation: true\n---\n'
                '# Probe\n!`touch SHOULD_NOT_EXIST`\n\n'
                '"${CLAUDE_PROJECT_DIR}" "${CLAUDE_SKILL_DIR}/references/a.md"\n',
                encoding="utf-8")
            result = subprocess.run([sys.executable, str(root / "scripts/studio.py"), "skill", "probe"],
                                    cwd=tmp, capture_output=True, text=True, encoding="utf-8", check=True)
            self.assertIn("Explicit invocation required", result.stdout)
            self.assertIn("```bash\ntouch SHOULD_NOT_EXIST\n```", result.stdout)
            self.assertIn('"." ".claude/skills/probe/references/a.md"', result.stdout)
            self.assertNotIn("model: opus", result.stdout)
            self.assertFalse((Path(tmp) / "SHOULD_NOT_EXIST").exists())
            self.assertFalse((root / "SHOULD_NOT_EXIST").exists())

    def test_unterminated_frontmatter_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text("---\nname: broken\n", encoding="utf-8")
            original = studio.ROOT
            try:
                studio.ROOT = Path(tmp)
                with self.assertRaisesRegex(ValueError, "Unterminated frontmatter"):
                    studio.read_document(path)
            finally:
                studio.ROOT = original

    def test_native_entrypoints_resolve_shared_instructions(self):
        for relative in (".agents/skills/studio/SKILL.md", ".grok/skills/studio/SKILL.md"):
            path = ROOT / relative
            header, body = studio.read_document(path)
            self.assertIn("name: studio", header)
            self.assertIn("description:", header)
            self.assertEqual(path.parents[3], ROOT)
        self.assertIn(".agents/skills/studio/SKILL.md", body)


if __name__ == "__main__":
    unittest.main()
