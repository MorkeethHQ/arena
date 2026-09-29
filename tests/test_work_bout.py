import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JUDGE = ROOT / "scripts" / "judge_work_bout"
FIXTURE = ROOT / "examples" / "BOUT-005"


class WorkBoutTest(unittest.TestCase):
    def run_judge(self, fixture: Path, output: Path):
        return subprocess.run(
            [sys.executable, str(JUDGE), str(fixture / "work-bout.json"), "--output", str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_fixture_emits_source_bound_result_and_offline_replay(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "generated"
            process = self.run_judge(FIXTURE, output)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads((output / "result.json").read_text(encoding="utf-8"))
            replay = (output / "results.html").read_text(encoding="utf-8")

            self.assertEqual(result["protocol"], "arena-real-work-v1")
            self.assertEqual(result["sample"], {"setups": 2, "distinct_tasks": 1})
            self.assertEqual(
                result["ordering_basis"],
                ["verified_completion", "acceptance_passes", "fewer_human_or_auth_stops"],
            )
            self.assertEqual(result["runs"][0]["id"], "setup-review-loop")
            self.assertTrue(result["runs"][0]["verified_completion"])
            self.assertFalse(result["runs"][1]["verified_completion"])
            self.assertTrue(
                all(event["evidence_exists"] for run in result["runs"] for event in run["action_tape"])
            )
            self.assertTrue(all(module["golden_bot"] is False for module in result["action_modules"]))
            self.assertIn("1 distinct task", result["action_modules"][0]["admission_reason"])
            self.assertIn("Popularity, separate", replay)
            self.assertIn("not a general setup leaderboard", replay)
            self.assertNotIn("https://", replay)
            self.assertNotIn("http://", replay)

    def test_missing_tape_evidence_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = Path(temp) / "BOUT-005"
            shutil.copytree(FIXTURE, fixture)
            tape_path = fixture / "runs" / "setup-direct-edit" / "action-tape.json"
            tape = json.loads(tape_path.read_text(encoding="utf-8"))
            tape[0]["evidence"] = "missing.txt"
            tape_path.write_text(json.dumps(tape, indent=2) + "\n", encoding="utf-8")
            process = self.run_judge(fixture, Path(temp) / "out")
            self.assertEqual(process.returncode, 2)
            self.assertIn("event evidence is missing", process.stderr)

    def test_popularity_cannot_change_outcome_order(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = Path(temp) / "BOUT-005"
            shutil.copytree(FIXTURE, fixture)
            brief_path = fixture / "work-bout.json"
            brief = json.loads(brief_path.read_text(encoding="utf-8"))
            brief["runs"][1]["popularity"] = {"downloads": 999999999, "basis": "test-only mutation"}
            brief_path.write_text(json.dumps(brief, indent=2) + "\n", encoding="utf-8")
            output = Path(temp) / "out"
            process = self.run_judge(fixture, output)
            self.assertEqual(process.returncode, 0, process.stderr)
            result = json.loads((output / "result.json").read_text(encoding="utf-8"))
            self.assertEqual(result["runs"][0]["id"], "setup-review-loop")


if __name__ == "__main__":
    unittest.main()
