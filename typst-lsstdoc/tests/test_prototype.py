"""Smoke tests for the Typst lsstdoc prototype."""

from __future__ import annotations

import ast
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from shutil import copytree, ignore_patterns

import yaml

REPOSITORY = Path(__file__).resolve().parents[2]

# Match the repository convention of importing the bin scripts directly
# (CI runs pytest with PYTHONPATH=bin) while keeping plain unittest
# discovery working.
if str(REPOSITORY / "bin") not in sys.path:
    sys.path.insert(0, str(REPOSITORY / "bin"))

from authorutils import check_orcid  # noqa: E402

PROTOTYPE = REPOSITORY / "typst-lsstdoc"
FONT_PATHS = [PROTOTYPE / "fonts"]

# Inline author arguments shared by the fixture documents.
SINGLE_AUTHOR_ARGS = (
    "  authors: (\n"
    "    (\n"
    '      internal_id: "example",\n'
    '      given_name: "Ada",\n'
    '      family_name: "Lovelace",\n'
    '      display_name: "Ada Lovelace",\n'
    "      orcid: none,\n"
    '      affiliations: ("INST",),\n'
    "    ),\n"
    "  ),\n"
    '  affiliations: (INST: (name: "Example Institute", address: "Tucson", ror: none)),\n'
)


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
        root: Path = REPOSITORY,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            "typst",
            "compile",
            "--root",
            str(root),
            "--font-path",
            ":".join(str(path) for path in FONT_PATHS),
        ]
        if pdf_standard:
            command.extend(("--pdf-standard", pdf_standard))
        for value in inputs:
            command.extend(("--input", value))
        command.extend((str(source), str(output)))
        return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_features_example_compiles(self) -> None:
        output = self.tempdir / "features.pdf"
        result = self.compile(
            PROTOTYPE / "examples/features.typ",
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
            # The running header must not leak stray punctuation.
            self.assertNotRegex(extracted, r"(?m)^,$")
        if qpdf := shutil.which("qpdf"):
            qdf = self.tempdir / "features-qdf.pdf"
            subprocess.run(
                [qpdf, "--qdf", "--object-streams=disable", str(output), str(qdf)],
                text=True,
                capture_output=True,
                check=True,
            )
            structure = qdf.read_bytes().decode("latin-1")
            self.assertIn("/Contents (DMTN-001)", structure)
            self.assertIn("/Contents (technical-note series)", structure)

    def test_document_states(self) -> None:
        for status in ("draft", "released", "obsolete"):
            with self.subTest(status=status):
                output = self.tempdir / f"{status}.pdf"
                result = self.compile(
                    PROTOTYPE / "examples/state.typ",
                    output,
                    f"status={status}",
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue(output.exists())

    def test_bibliography_style_option(self) -> None:
        source = self.tempdir / "bib-style.typ"
        source.write_text(
            '#import "../../src/lsstdoc.typ": lsstdoc\n'
            "#show: lsstdoc.with(\n"
            '  title: "Bibliography Style Test",\n'
            '  id: "DMTN-999",\n'
            '  series: "DMTN",\n'
            '  date: "2026-07-16",\n' + SINGLE_AUTHOR_ARGS + "  toc: false,\n"
            '  bibliography: (read("../../examples/references.bib", encoding: none),),\n'
            '  bibliography-style: "ieee",\n'
            ")\n"
            "= Test\n"
            "A citation @jenness-example.\n",
            encoding="utf-8",
        )
        result = self.compile(source, self.tempdir / "bib-style.pdf")
        self.assertEqual(result.returncode, 0, result.stderr)

    def write_doi_document(self, doi: str) -> Path:
        """Write a minimal document that sets the given DOI."""
        source = self.tempdir / "doi.typ"
        source.write_text(
            '#import "../../src/lsstdoc.typ": lsstdoc\n'
            "#show: lsstdoc.with(\n"
            '  title: "DOI Test",\n'
            '  id: "DMTN-999",\n'
            '  series: "DMTN",\n'
            '  date: "2026-07-16",\n' + SINGLE_AUTHOR_ARGS + "  toc: false,\n"
            f'  doi: "{doi}",\n'
            ")\n"
            "= Test\n",
            encoding="utf-8",
        )
        return source

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext is not installed")
    def test_doi_renders_once_as_link(self) -> None:
        source = self.write_doi_document("10.71929/example.71")
        output = self.tempdir / "doi.pdf"
        result = self.compile(source, output)
        self.assertEqual(result.returncode, 0, result.stderr)
        extracted = subprocess.run(
            ["pdftotext", str(output), "-"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(extracted.count("https://doi.org/10.71929/example.71"), 1)
        self.assertEqual(extracted.count("https://doi.org/"), 1)

    def test_url_prefixed_doi_is_rejected(self) -> None:
        source = self.write_doi_document("https://doi.org/10.71929/example.71")
        result = self.compile(source, self.tempdir / "doi-bad.pdf")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bare identifier", result.stderr)

    def test_change_record_accepts_non_string_values(self) -> None:
        source = self.tempdir / "changes.typ"
        source.write_text(
            '#import "../../src/change-record.typ": render-change-record\n'
            "#render-change-record((\n"
            '  (version: 0.1, date: "2026-01-01", description: "Start", author: "A Person"),\n'
            "))\n",
            encoding="utf-8",
        )
        result = self.compile(source, self.tempdir / "changes.pdf")
        self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext is not installed")
    def test_two_authors_have_no_comma_before_and(self) -> None:
        source = self.tempdir / "two-authors.typ"
        source.write_text(
            '#import "../../src/lsstdoc.typ": lsstdoc\n'
            "#show: lsstdoc.with(\n"
            '  title: "Two Author Test",\n'
            '  id: "DMTN-999",\n'
            '  series: "DMTN",\n'
            '  date: "2026-07-16",\n'
            "  authors: (\n"
            '    (internal_id: "a", display_name: "Ada Lovelace", affiliations: ("INST",)),\n'
            '    (internal_id: "b", display_name: "Grace Hopper", affiliations: ("INST",)),\n'
            "  ),\n"
            '  affiliations: (INST: (name: "Example Institute", address: "Tucson", ror: none)),\n'
            "  toc: false,\n"
            ")\n"
            "= Test\n",
            encoding="utf-8",
        )

        output = self.tempdir / "two-authors.pdf"
        result = self.compile(source, output)
        self.assertEqual(result.returncode, 0, result.stderr)
        extracted = subprocess.run(
            ["pdftotext", str(output), "-"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        self.assertIn("Ada Lovelace", extracted)
        self.assertNotRegex(extracted, r"Lovelace\s*,")

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext is not installed")
    def test_technote_toml_example_compiles(self) -> None:
        output = self.tempdir / "technote.pdf"
        result = self.compile(PROTOTYPE / "examples/technote.typ", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        extracted = subprocess.run(
            ["pdftotext", str(output), "-"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        self.assertIn("SQR-999", extracted)
        self.assertIn("SQuaRE Technical Note", extracted)
        self.assertIn("Ada Lovelace", extracted)
        self.assertIn("Grace Hopper", extracted)
        # The shared affiliation is deduplicated to a single entry.
        self.assertEqual(extracted.count("Example Institute"), 1)
        # A stable technote maps to released: no draft furniture.
        self.assertNotIn("D R A F T", extracted)

    def test_technote_example_is_self_contained(self) -> None:
        """The technote flow must not read outside the template subtree."""
        output = self.tempdir / "standalone.pdf"
        result = self.compile(
            PROTOTYPE / "examples/technote.typ",
            output,
            root=PROTOTYPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_vendored_package_template_scaffold(self) -> None:
        """The template scaffold compiles through a vendored @preview package.

        This mirrors what ``typst init @preview/rubin-technote`` produces: the
        files from the manifest's template path in a fresh directory, importing
        the package.
        """
        package_dir = self.tempdir / "packages/preview/rubin-technote/0.1.0"
        copytree(PROTOTYPE, package_dir, ignore=ignore_patterns("tmp", "output", "tests"))

        manifest = tomllib.loads((PROTOTYPE / "typst.toml").read_text(encoding="utf-8"))
        template = manifest["template"]
        workdir = self.tempdir / "scaffold"
        copytree(PROTOTYPE / template["path"], workdir)

        command = [
            "typst",
            "compile",
            "--root",
            str(workdir),
            "--package-path",
            str(self.tempdir / "packages"),
            "--font-path",
            str(package_dir / "fonts"),
            str(workdir / template["entrypoint"]),
            str(self.tempdir / "scaffold.pdf"),
        ]
        result = subprocess.run(command, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_manual_compiles(self) -> None:
        """The user guide builds and is typeset with the template itself."""
        output = self.tempdir / "manual.pdf"
        result = self.compile(
            PROTOTYPE / "docs/manual.typ",
            output,
            root=PROTOTYPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        if pdftotext := shutil.which("pdftotext"):
            extracted = subprocess.run(
                [pdftotext, str(output), "-"],
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            self.assertIn("Change Record", extracted)
            self.assertIn("Contents", extracted)
            self.assertIn("Admonitions", extracted)
            self.assertIn("API reference", extracted)
            self.assertIn("References", extracted)

    @unittest.skipUnless(shutil.which("pdftotext"), "pdftotext is not installed")
    def test_technote_toml_maps_doi(self) -> None:
        output = self.tempdir / "technote-doi.pdf"
        result = self.compile(PROTOTYPE / "examples/technote.typ", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        extracted = subprocess.run(
            ["pdftotext", str(output), "-"],
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(extracted.count("https://doi.org/10.71929/rubin/example.999"), 1)

    def test_front_matter_is_queryable(self) -> None:
        """Tooling can extract the front matter with typst query."""
        result = subprocess.run(
            [
                "typst",
                "query",
                "--root",
                str(REPOSITORY),
                "--font-path",
                ":".join(str(path) for path in FONT_PATHS),
                str(PROTOTYPE / "examples/technote.typ"),
                "<rubin-technote>",
                "--field",
                "value",
                "--one",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        front_matter = json.loads(result.stdout)
        self.assertEqual(front_matter["id"], "SQR-999")
        self.assertEqual(front_matter["series"], "SQR")
        self.assertEqual(front_matter["status"], "released")
        self.assertEqual(front_matter["title"], "Reusing Documenteer Technote Metadata")
        self.assertIn("Documenteer", json.dumps(front_matter["abstract"]))

    def test_technote_toml_unknown_state_rejected(self) -> None:
        source = self.tempdir / "state.typ"
        (self.tempdir / "technote.toml").write_text(
            "[technote]\n"
            'id = "SQR-999"\n'
            'series_id = "SQR"\n'
            "date_created = 2026-07-16T00:00:00Z\n"
            "[technote.status]\n"
            'state = "other"\n'
            "[[technote.authors]]\n"
            'name = {given = "Ada", family = "Lovelace"}\n',
            encoding="utf-8",
        )
        source.write_text(
            '#import "../../src/lsstdoc.typ": lsstdoc\n'
            '#import "../../src/technote-toml.typ": technote-args\n'
            "#show: lsstdoc.with(\n"
            '  ..technote-args(toml("technote.toml")),\n'
            '  title: "Unknown State Test",\n'
            "  toc: false,\n"
            ")\n"
            "= Test\n",
            encoding="utf-8",
        )
        result = self.compile(source, self.tempdir / "state.pdf")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("technote status state", result.stderr)

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

    def test_package_manifest_is_universe_ready(self) -> None:
        manifest = tomllib.loads((PROTOTYPE / "typst.toml").read_text(encoding="utf-8"))
        package = manifest["package"]
        self.assertEqual(package["name"], "rubin-technote")
        self.assertEqual(package["license"], "MIT")
        self.assertTrue((PROTOTYPE / "LICENSE").exists())
        self.assertNotIn("typst", package["description"].lower())
        self.assertLessEqual(len(package["description"]), 60)
        self.assertTrue(package["categories"])
        self.assertIn("tests", package["exclude"])

        template = manifest["template"]
        entrypoint = PROTOTYPE / template["path"] / template["entrypoint"]
        self.assertTrue(entrypoint.exists())

        thumbnail = PROTOTYPE / template["thumbnail"]
        self.assertTrue(thumbnail.exists())
        header = thumbnail.read_bytes()[:24]
        self.assertEqual(header[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", header[16:24])
        self.assertGreaterEqual(max(width, height), 1080)
        self.assertLessEqual(thumbnail.stat().st_size, 3 * 1024 * 1024)

    def test_controlled_series_reference_valid_series(self) -> None:
        data = yaml.safe_load((PROTOTYPE / "data/series.yaml").read_text(encoding="utf-8"))
        controlled = data["controlled"]
        self.assertTrue(set(controlled).issubset(data["series"]))
        self.assertIn("LDM", controlled)
        self.assertIn("RDO", controlled)
        self.assertNotIn("DMTN", controlled)

    def test_orcid_validation(self) -> None:
        self.assertEqual(check_orcid("000000015982167X"), "0000-0001-5982-167X")
        with self.assertRaisesRegex(ValueError, "does not match standard form"):
            check_orcid("https://orcid.org/0000-0001-5982-167X")


if __name__ == "__main__":
    unittest.main()
