"""Integration tests for the core translate_po_file function."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import polib

from translator.translator import translate_po_file


def _make_po_file(entries: list[dict]) -> str:
    """Create a temporary .po file and return its path."""
    po = polib.POFile()
    po.metadata = {"Content-Type": "text/plain; charset=UTF-8"}
    for e in entries:
        entry = polib.POEntry(
            msgid=e.get("msgid", ""),
            msgstr=e.get("msgstr", ""),
        )
        if "flags" in e:
            entry.flags = e["flags"]
        po.append(entry)
    tmp = tempfile.NamedTemporaryFile(suffix=".po", delete=False)
    po.save(tmp.name)
    return tmp.name


class TestTranslatePoFile:
    def test_translates_empty_entry(self) -> None:
        input_path = _make_po_file([{"msgid": "Save", "msgstr": ""}])
        output_path = input_path.replace(".po", "_out.po")

        with patch("translator.translator.translate_google", return_value="Salva"):
            translate_po_file(input_path, output_path)

        result = polib.pofile(output_path)
        assert result[0].msgstr == "Salva"

    def test_skips_already_translated(self) -> None:
        input_path = _make_po_file([{"msgid": "Save", "msgstr": "Salva"}])
        output_path = input_path.replace(".po", "_out.po")

        with patch("translator.translator.translate_google") as mock_translate:
            translate_po_file(input_path, output_path)

        mock_translate.assert_not_called()

    def test_clears_fuzzy_flag(self) -> None:
        input_path = _make_po_file(
            [{"msgid": "Save", "msgstr": "Salva", "flags": ["fuzzy"]}]
        )
        output_path = input_path.replace(".po", "_out.po")

        with patch("translator.translator.translate_google", return_value="Salva"):
            translate_po_file(input_path, output_path)

        result = polib.pofile(output_path)
        assert "fuzzy" not in result[0].flags

    def test_output_file_is_created(self) -> None:
        input_path = _make_po_file([{"msgid": "Hello", "msgstr": ""}])
        output_path = input_path.replace(".po", "_out.po")

        with patch("translator.translator.translate_google", return_value="Ciao"):
            translate_po_file(input_path, output_path)

        assert Path(output_path).exists()
