"""Technical term protection utilities.

Prevents technical terms from being altered during translation
by replacing them with safe placeholders before the API call
and restoring them afterward.
"""

import re

TECHNICAL_TERMS: list[str] = [
    "API", "REST", "HTTP", "HTTPS", "URL", "JSON", "XML", "HTML", "CSS",
    "JavaScript", "Python", "SQL", "database", "backend", "frontend",
    "framework", "middleware", "endpoint", "token", "OAuth", "JWT",
    "webhook", "payload", "request", "response", "server", "client",
    "cache", "cookie", "session", "login", "logout", "email", "username",
    "password", "hash", "debug", "log", "error", "warning", "info",
    "status", "config", "deploy", "build", "test", "staging", "production",
]


def protect_technical_terms(text: str) -> tuple[str, dict[str, str]]:
    """Replace technical terms with placeholders.

    Args:
        text: The original source string.

    Returns:
        A tuple of (protected_text, placeholders_mapping).
    """
    placeholders: dict[str, str] = {}
    protected = text
    for i, term in enumerate(TECHNICAL_TERMS):
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        placeholder = f"__TECH_{i}__"
        if pattern.search(protected):
            placeholders[placeholder] = term
            protected = pattern.sub(placeholder, protected)
    return protected, placeholders


def restore_technical_terms(text: str, placeholders: dict[str, str]) -> str:
    """Restore original technical terms from placeholders.

    Args:
        text: Translated text containing placeholders.
        placeholders: Mapping returned by protect_technical_terms.

    Returns:
        Text with placeholders replaced by original terms.
    """
    restored = text
    for placeholder, term in placeholders.items():
        restored = restored.replace(placeholder, term)
    return restored


def capitalize_sentences(text: str) -> str:
    """Capitalize the first letter of each sentence.

    Args:
        text: Input string, possibly multi-sentence.

    Returns:
        String with every sentence capitalized.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    capitalized = []
    for sentence in sentences:
        if sentence:
            sentence = (
                sentence[0].upper() + sentence[1:]
                if len(sentence) > 1
                else sentence.upper()
            )
            capitalized.append(sentence)
    result = " ".join(capitalized)
    return result[0].upper() + result[1:] if result else result
