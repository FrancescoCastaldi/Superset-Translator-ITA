"""Tests for the Google Translate client module."""

from unittest.mock import MagicMock, patch

from translator.google import translate_google


class TestTranslateGoogle:
    def test_returns_translated_text(self) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = [[["Ciao mondo", "Hello world"]]]
        mock_response.raise_for_status = MagicMock()

        with patch("translator.google.requests.get", return_value=mock_response):
            result = translate_google("Hello world")

        assert result == "Ciao mondo"

    def test_falls_back_on_network_error(self) -> None:
        with patch("translator.google.requests.get", side_effect=ConnectionError):
            result = translate_google("Hello world")

        assert result == "Hello world"

    def test_technical_terms_preserved(self) -> None:
        mock_response = MagicMock()
        mock_response.json.return_value = [
            [[["Controlla __TECH_0__ docs", "Check API docs"]]]
        ]
        mock_response.raise_for_status = MagicMock()

        with patch("translator.google.requests.get", return_value=mock_response):
            result = translate_google("Check API docs")

        assert "API" in result
