"""Exercise the real CLI with isolated task files."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


APP = Path(__file__).resolve().parents[1] / "todo.py"


class TodoTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.file = Path(self.directory.name) / "tasks.json"

    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(APP), "--file", str(self.file), *arguments],
            capture_output=True, text=True, timeout=5,
        )

    def successful(self, *arguments):
        result = self.run_cli(*arguments)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def state(self):
        return json.loads(self.file.read_text(encoding="utf-8"))

    def test_empty_list_does_not_create_file(self):
        self.assertEqual(self.successful("list"), "No tasks yet.\n")
        self.assertFalse(self.file.exists())

    def test_add_persists_and_trims_title(self):
        self.successful("add", "  Read chapter 3  ")
        self.assertEqual(self.state(), {
            "next_id": 2,
            "tasks": [{"id": 1, "title": "Read chapter 3", "done": False}],
        })
        self.assertEqual(self.successful("list"), "1. [ ] Read chapter 3\n")

    def test_unicode_title_survives_restart(self):
        self.successful("add", "Les om køer")
        self.assertEqual(self.successful("list"), "1. [ ] Les om køer\n")

    def test_empty_title_is_rejected_without_write(self):
        result = self.run_cli("add", "")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Title cannot be empty", result.stderr)
        self.assertFalse(self.file.exists())

    @unittest.expectedFailure
    def test_whitespace_only_title_is_rejected(self):
        # Known demo defect: validation currently happens before trimming.
        self.successful("add", "Keep this task")
        before = self.file.read_bytes()
        result = self.run_cli("add", "   ")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.file.read_bytes(), before)

    def test_accepts_eighty_character_title(self):
        self.successful("add", "a" * 80)
        self.assertEqual(self.state()["tasks"][0]["title"], "a" * 80)

    def test_rejects_eighty_one_character_title_without_write(self):
        self.successful("add", "Keep this task")
        before = self.file.read_bytes()
        result = self.run_cli("add", "a" * 81)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Title must be at most", result.stderr)
        self.assertEqual(self.file.read_bytes(), before)

    def test_done_persists_completed_status(self):
        self.successful("add", "Read chapter 3")
        self.successful("done", "1")
        self.assertTrue(self.state()["tasks"][0]["done"])
        self.assertEqual(self.successful("list"), "1. [x] Read chapter 3\n")

    def test_repeating_done_is_harmless(self):
        self.successful("add", "Read chapter 3")
        self.successful("done", "1")
        self.successful("done", "1")
        self.assertEqual(len(self.state()["tasks"]), 1)
        self.assertTrue(self.state()["tasks"][0]["done"])

    def test_remove_does_not_reuse_ids(self):
        self.successful("add", "First")
        self.successful("remove", "1")
        self.assertEqual(self.successful("list"), "No tasks yet.\n")
        self.successful("add", "Second")
        self.assertEqual(self.state()["tasks"], [
            {"id": 2, "title": "Second", "done": False},
        ])

    def test_unknown_ids_do_not_change_tasks(self):
        self.successful("add", "Keep this task")
        before = self.file.read_bytes()
        for command in ("done", "remove"):
            with self.subTest(command=command):
                result = self.run_cli(command, "99")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Task 99 not found", result.stderr)
                self.assertEqual(self.file.read_bytes(), before)

    def test_invalid_json_is_not_overwritten(self):
        self.file.write_text("not json", encoding="utf-8")
        result = self.run_cli("add", "Read chapter 3")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid task file", result.stderr)
        self.assertEqual(self.file.read_text(encoding="utf-8"), "not json")

    def test_wrong_file_structure_is_not_overwritten(self):
        self.file.write_text("[]", encoding="utf-8")
        result = self.run_cli("list")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid task file", result.stderr)
        self.assertEqual(self.file.read_text(encoding="utf-8"), "[]")

    def test_help_describes_available_commands(self):
        output = self.successful("--help")
        for command in ("add", "list", "done", "remove", "--file"):
            self.assertIn(command, output)


if __name__ == "__main__":
    unittest.main()
