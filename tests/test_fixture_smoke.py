import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JUDGE = ROOT / "scripts" / "judge"


class FixtureSmokeTest(unittest.TestCase):
    def test_example_bouts(self):
        for bout_id in ("BOUT-001", "BOUT-002"):
            with self.subTest(bout_id=bout_id), tempfile.TemporaryDirectory() as temp:
                fixture = ROOT / "examples" / bout_id
                output = Path(temp) / bout_id
                process = subprocess.run(
                    [sys.executable, str(JUDGE), str(fixture / "bout.json"), "--output", str(output)],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(process.returncode, 0, process.stderr)
                summary = json.loads(process.stdout)
                expected = json.loads((fixture / "expected.json").read_text(encoding="utf-8"))
                result_path = output / "result.json"
                card_path = output / "result-card.html"
                self.assertTrue(result_path.is_file())
                self.assertTrue(card_path.is_file())
                self.assertIn("<!doctype html>", card_path.read_text(encoding="utf-8").lower())

                result = json.loads(result_path.read_text(encoding="utf-8"))
                self.assertEqual(summary["status"], expected["status"])
                self.assertEqual(summary["winner"], expected["winner"])
                self.assertEqual(result["decision"]["status"], expected["status"])
                self.assertEqual(result["decision"]["winner"], expected["winner"])
                for fighter in result["fighters"]:
                    self.assertFalse(fighter["dq"], fighter["dq_reasons"])
                    self.assertEqual(
                        fighter["passes"], expected["rubric_passes"][fighter["id"]]
                    )


if __name__ == "__main__":
    unittest.main()
