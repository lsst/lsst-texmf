"""Smoke tests for the Typst lsstdoc prototype."""

from __future__ import annotations

import ast
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPOSITORY = Path(__file__).resolve().parents[2]

# Match the repository convention of importing the bin scripts directly
# (CI runs pytest with PYTHONPATH=bin) while keeping plain unittest
# discovery working.
if str(REPOSITORY / "bin") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "bin"))

from authorutils import check_orcid  # noqa: E402

PROTOTYPE = REPOSITORY / "typst-lsstdoc"
FONT_PATHS = [
    REPOSITORY / "texmf/fonts/truetype/public/opensans",
    REPOSITORY / "texmf/fonts/truetype/public/Inconsolata",
    REPOSITORY / "texmf/fonts/opentype/public/xits",
]


def load_bibtools_series() -> dict[str, str]:
    """Read the literal TN_SERIES mapping without importing bibtools."""
    tree = ast.parse((REPOSITORY / "bin/bibtools.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "TN_SERIES" for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AssertionError("TN_SERIES was not found in bin/bibtools.py")


@unittest.skipUnless(shutil.which("typst"), "Typst is not installed")
class TypstCompileTest(unittest.TestCase):
    """Compile the representative and state-focused documents."""

    def setUp(self) -> None:
        (PROTOTYPE / "tmp").mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=PROTOTYPE / "tmp")
        self.tempdir = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def compile(
        self,
        source: Path,
        output: Path,
        *inputs: str,
        pdf_standard: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            "typst",
            "compile",
            "--root",
            str(REPOSITORY),
            "--font-path",
            ":".join(str(path) for path in FONT_PATHS),
        ]
        if pdf_standard:
            command.extend(("--pdf-standard", pdf_standard))
        for value in inputs:
            command.extend(("--input", value))
        command.extend((str(source), str(output)))
        return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_full_prototype_compiles(self) -> None:
        output = self.tempdir / "prototype.pdf"
        result = self.compile(
            PROTOTYPE / "examples/prototype.typ",
            output,
            pdf_standard="ua-1",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertGreater(output.stat().st_size, 10_000)
        if pdftotext := shutil.which("pdftotext"):
            extracted = subprocess.run(
                [pdftotext, str(output), "-"],
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            self.assertIn("DMTN-001", extracted)
            self.assertIn("technical-note series", extracted)
            self.assertIn("Tidy Data", extracted)
            self.assertNotIn("Software Carpentry", extracted)
        if qpdf := shutil.which("qpdf"):
            qdf = self.tempdir / "prototype-qdf.pdf"
            subprocess.run(
                [qpdf, "--qdf", "--object-streams=disable", str(output), str(qdf)],
                text=True,
                capture_output=True,
                check=True,
            )
            structure = qdf.read_bytes().decode("latin-1")
            self.assertRegex(structure, r"(?s)/Contents \(DMTN-001\).*?/Dest")
            self.assertRegex(structure, r"(?s)/Contents \(technical-note series\).*?/Dest")

    def test_document_states_and_generated_authors(self) -> None:
        generated = self.tempdir / "authors.yaml"
        export = subprocess.run(
            [
                "python3",
                str(REPOSITORY / "bin/db2authors.py"),
                "--mode",
                "typst-yaml",
                "--authors",
                str(PROTOTYPE / "examples/author-ids.yaml"),
                "--output",
                str(generated),
            ],
            cwd=REPOSITORY,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(export.returncode, 0, export.stderr)
        exported = yaml.safe_load(generated.read_text(encoding="utf-8"))
        self.assertEqual(
            [author["internal_id"] for author in exported["authors"]],
            ["jennesst", "acostae", "acquavivav"],
        )
        self.assertEqual(list(exported["affiliations"]), ["RubinObs", "CCA", "CUNYCT"])
        self.assertEqual(exported["authors"][0]["orcid"], "0000-0001-5982-167X")
        relative_authors = generated.relative_to(PROTOTYPE / "examples", walk_up=True)

        for status in ("draft", "released", "obsolete"):
            with self.subTest(status=status):
                output = self.tempdir / f"{status}.pdf"
                result = self.compile(
                    PROTOTYPE / "examples/state.typ",
                    output,
                    f"status={status}",
                    f"authors={relative_authors}",
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(output.exists())

    def test_invalid_document_state_fails_clearly(self) -> None:
        result = self.compile(
            PROTOTYPE / "examples/state.typ",
            self.tempdir / "invalid.pdf",
            "status=withdrawn",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unsupported document status: withdrawn", result.stderr)


class MetadataTest(unittest.TestCase):
    """Validate shared mappings and generated author structure."""

    def test_series_matches_bibtools(self) -> None:
        expected = load_bibtools_series()
        actual = yaml.safe_load((PROTOTYPE / "data/series.yaml").read_text(encoding="utf-8"))["series"]
        self.assertEqual(actual, expected)

    def test_controlled_series_reference_valid_series(self) -> None:
        data = yaml.safe_load((PROTOTYPE / "data/series.yaml").read_text(encoding="utf-8"))
        controlled = data["controlled"]
        self.assertTrue(set(controlled).issubset(data["series"]))
        self.assertIn("LDM", controlled)
        self.assertIn("RDO", controlled)
        self.assertNotIn("DMTN", controlled)

    def test_example_author_references_resolve(self) -> None:
        people = yaml.safe_load((PROTOTYPE / "examples/authors.yaml").read_text(encoding="utf-8"))
        affiliations = people["affiliations"]
        for author in people["authors"]:
            for affiliation in author["affiliations"]:
                self.assertIn(affiliation, affiliations)

    def test_orcid_validation(self) -> None:
        self.assertEqual(check_orcid("000000015982167X"), "0000-0001-5982-167X")
        with self.assertRaisesRegex(ValueError, "does not match standard form"):
            check_orcid("https://orcid.org/0000-0001-5982-167X")


if __name__ == "__main__":
    unittest.main()
