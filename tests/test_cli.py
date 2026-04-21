import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class CliTest(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "main.py", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_decode_command(self) -> None:
        completed = self._run("decode", "00412820")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(
            completed.stdout.strip(),
            "\n".join(
                [
                    "family: R",
                    "opcode: 000000",
                    "rs: 00010 ($2)",
                    "rt: 00001 ($1)",
                    "rd: 00101 ($5)",
                    "shamt: 00000",
                    "funct: 100000",
                    "assembly: add $5, $2, $1",
                ]
            ),
        )

    def test_encode_command(self) -> None:
        completed = self._run("encode", "sw $7, 5($5)")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(
            completed.stdout.strip(),
            "\n".join(
                [
                    "hex: aca70005",
                    "binary: 10101100101001110000000000000101",
                ]
            ),
        )

    def test_decode_reports_unsupported_opcode(self) -> None:
        completed = self._run("decode", "08000010")
        self.assertEqual(completed.returncode, 1)
        self.assertIn("error: unsupported primary opcode 0x02", completed.stdout)


if __name__ == "__main__":
    unittest.main()
