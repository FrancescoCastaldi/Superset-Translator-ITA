"""Core PO file translation logic.

Orchestrates reading a .po file, translating each entry via
Google Translate, handling plural forms, and saving the result.
"""

import time

import polib

from .google import translate_google

_SLEEP_INTERVAL = 0.1  # seconds between API calls to avoid rate-limiting


def _translate_entry(entry: polib.POEntry, count: int, total: int) -> None:
    """Translate a single PO entry in-place (singular or plural).

    Args:
        entry: The polib entry to translate.
        count: Current entry index (for progress display).
        total: Total number of entries (for progress display).
    """
    if entry.msgid_plural:
        _translate_plural_entry(entry, count, total)
    else:
        _translate_singular_entry(entry, count, total)


def _translate_singular_entry(entry: polib.POEntry, count: int, total: int) -> None:
    if not entry.msgstr or "fuzzy" in entry.flags:
        preview = entry.msgid[:50] + "..." if len(entry.msgid) > 50 else entry.msgid
        translated = translate_google(entry.msgid)
        entry.msgstr = translated
        if "fuzzy" in entry.flags:
            entry.flags.remove("fuzzy")
        print(f"  ✓ {count}/{total} - '{preview}'")
        time.sleep(_SLEEP_INTERVAL)
    else:
        print(f"  - {count}/{total} - Already translated")


def _translate_plural_entry(entry: polib.POEntry, count: int, total: int) -> None:
    forms_to_translate: dict[int, str] = {
        0: entry.msgid,
        1: entry.msgid_plural,
    }
    for idx in entry.msgstr_plural:
        if idx > 1:
            forms_to_translate[idx] = entry.msgstr_plural[idx]

    needs_translation = (
        not entry.msgstr_plural
        or any(not v for v in entry.msgstr_plural.values())
        or "fuzzy" in entry.flags
    )

    if not needs_translation:
        print(f"  - {count}/{total} - Already translated (plural)")
        return

    for idx, source_text in forms_to_translate.items():
        if not entry.msgstr_plural.get(idx) or "fuzzy" in entry.flags:
            translated = translate_google(source_text)
            entry.msgstr_plural[idx] = translated
            label = "singular" if idx == 0 else f"plural[{idx}]"
            preview = source_text[:50] + "..." if len(source_text) > 50 else source_text
            print(f"    ↳ [{label}] '{preview}' → '{translated[:50]}'")
            time.sleep(_SLEEP_INTERVAL)

    if "fuzzy" in entry.flags:
        entry.flags.remove("fuzzy")

    print(f"  ✓ {count}/{total} - [PLURAL] '{entry.msgid[:50]}'")


def translate_po_file(input_file: str, output_file: str) -> None:
    """Translate all untranslated entries in a PO file.

    Reads *input_file*, translates every entry that is either empty
    or flagged as ``fuzzy``, and writes the result to *output_file*.

    Args:
        input_file: Path to the source ``.po`` file (English).
        output_file: Path where the translated ``.po`` file is saved.
    """
    po = polib.pofile(input_file)
    total = len(po)
    print(f"Found {total} entries in '{input_file}'")

    for count, entry in enumerate(po, start=1):
        try:
            _translate_entry(entry, count, total)
        except Exception as exc:  # noqa: BLE001
            print(f"  ✗ Error on '{entry.msgid[:50]}': {exc}")

    print(f"\nSaving to '{output_file}'...")
    po.save(output_file)
    print("Done!")
