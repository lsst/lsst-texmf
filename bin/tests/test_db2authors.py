"""Tests for db2authors author list generation."""

import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from db2authors import AASTeX, AuthorFactory

REPOSITORY = Path(__file__).resolve().parents[2]
SCRIPT = REPOSITORY / "bin" / "db2authors.py"

TEST_AUTHORDB = {
    "affiliations": {
        "_": {
            "institute": "Placeholder used for collective author that will not be shown",
            "department": None,
            "email": None,
            "ror_id": None,
            "address": None,
        },
        "INST": {
            "institute": "Example Institute",
            "department": None,
            "email": "example.edu",
            "ror_id": None,
            "address": {
                "street": None,
                "city": "Tucson",
                "state": "Arizona",
                "postcode": None,
                "country_code": "US",
                "example_expanded": "Example Institute, Tucson, Arizona, US",
            },
        },
        "NOMAIL": {
            "institute": "Quiet Institute",
            "department": None,
            "email": None,
            "ror_id": None,
            "address": None,
        },
    },
    "authors": {
        "collab": {
            "given_name": "",
            "family_name": "Example Collaboration",
            "email": "",
            "orcid": None,
            "affil": ["_"],
            "altaffil": [],
        },
        "person": {
            "given_name": "Ada",
            "family_name": "Lovelace",
            "email": "ada",
            "orcid": None,
            "affil": ["INST"],
            "altaffil": [],
        },
        "quiet": {
            "given_name": "Quinn",
            "family_name": "Quiet",
            "email": "",
            "orcid": None,
            "affil": ["NOMAIL"],
            "altaffil": [],
        },
    },
}


class EmailWarningTest(unittest.TestCase):
    """Test that email warnings come from email-consuming generators."""

    def setUp(self) -> None:
        self.factory = AuthorFactory.from_authordb(TEST_AUTHORDB)

    def resolve(self, author_id: str) -> tuple:
        """Resolve one author, returning the author and captured stderr."""
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            author = self.factory.get_author(author_id)
        return author, stderr.getvalue()

    def test_get_author_does_not_warn(self) -> None:
        _, captured = self.resolve("quiet")
        self.assertEqual(captured, "")

    def test_email_generator_warns_for_unresolved_email(self) -> None:
        author, _ = self.resolve("quiet")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            AASTeX([author]).generate()
        self.assertIn("Unable to resolve email address for author 'quiet'", stderr.getvalue())

    def test_email_generator_does_not_warn_for_collective_author(self) -> None:
        author, _ = self.resolve("collab")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            AASTeX([author]).generate()
        self.assertEqual(stderr.getvalue(), "")


class OutputOptionTest(unittest.TestCase):
    """Test the --output command line option."""

    def run_script(self, *options: str, cwd: Path = REPOSITORY) -> subprocess.CompletedProcess:
        """Run db2authors.py with the given options."""
        return subprocess.run(
            [sys.executable, str(SCRIPT), *options],
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd,
        )

    def test_output_file_matches_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            author_list = Path(tmpdir) / "authors.yaml"
            author_list.write_text("- jennesst\n", encoding="utf-8")
            options = ("--mode", "lsstdoc", "--authors", str(author_list))

            stdout_run = self.run_script(*options)
            self.assertEqual(stdout_run.returncode, 0, stdout_run.stderr)

            output_file = Path(tmpdir) / "authors.tex"
            file_run = self.run_script(*options, "--output", str(output_file))
            self.assertEqual(file_run.returncode, 0, file_run.stderr)
            content = output_file.read_text(encoding="utf-8")

        self.assertTrue(content.endswith("\n"))
        self.assertEqual(content, stdout_run.stdout)

    def test_csvall_rejects_output_option(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_script("--mode", "csvall", "--output", "unused.csv", cwd=Path(tmpdir))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--output", result.stderr)


if __name__ == "__main__":
    unittest.main()
