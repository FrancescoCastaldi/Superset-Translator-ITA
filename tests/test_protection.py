"""Tests for the technical-term protection module."""

from translator.protection import (
    capitalize_sentences,
    protect_technical_terms,
    restore_technical_terms,
)


class TestProtectTechnicalTerms:
    def test_replaces_known_term(self) -> None:
        protected, placeholders = protect_technical_terms("Check the API docs")
        assert "API" not in protected
        assert any("API" in v for v in placeholders.values())

    def test_no_terms_returns_unchanged(self) -> None:
        protected, placeholders = protect_technical_terms("Hello world")
        assert protected == "Hello world"
        assert placeholders == {}

    def test_case_insensitive(self) -> None:
        protected, _ = protect_technical_terms("use the api endpoint")
        assert "api" not in protected.lower() or "__TECH_" in protected


class TestRestoreTechnicalTerms:
    def test_round_trip(self) -> None:
        original = "Configure the OAuth token via API"
        protected, placeholders = protect_technical_terms(original)
        restored = restore_technical_terms(protected, placeholders)
        # Every original term must appear in restored text
        for term in ["OAuth", "API"]:
            assert term in restored

    def test_empty_placeholders(self) -> None:
        assert restore_technical_terms("hello", {}) == "hello"


class TestCapitalizeSentences:
    def test_single_sentence(self) -> None:
        assert capitalize_sentences("hello world") == "Hello world"

    def test_multiple_sentences(self) -> None:
        result = capitalize_sentences("hello world. how are you?")
        assert result.startswith("Hello")

    def test_empty_string(self) -> None:
        assert capitalize_sentences("") == ""
