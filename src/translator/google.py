"""Google Translate unofficial API client.

Uses the free `gtx` endpoint — no API key required.
Rate-limiting is handled by the caller via sleep intervals.
"""

import requests

from .protection import (
    protect_technical_terms,
    restore_technical_terms,
    capitalize_sentences,
)

_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
_DEFAULT_TIMEOUT = 10


def translate_google(
    text: str,
    source_lang: str = "en",
    target_lang: str = "it",
) -> str:
    """Translate text using the Google Translate unofficial API.

    Technical terms are protected from translation via placeholder
    substitution. Falls back to the original text on any error.

    Args:
        text: The English source string.
        source_lang: BCP-47 source language code (default: ``"en"``).
        target_lang: BCP-47 target language code (default: ``"it"``).

    Returns:
        Translated string, or the original text if the request fails.
    """
    protected_text, placeholders = protect_technical_terms(text)
    params = {
        "client": "gtx",
        "sl": source_lang,
        "tl": target_lang,
        "dt": "t",
        "q": protected_text,
    }
    try:
        resp = requests.get(
            _TRANSLATE_URL, params=params, timeout=_DEFAULT_TIMEOUT
        )
        resp.raise_for_status()
        translated: str = resp.json()[0][0][0]
        translated = restore_technical_terms(translated, placeholders)
        return capitalize_sentences(translated)
    except Exception:  # noqa: BLE001
        return text
