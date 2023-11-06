import pytest

from fetch_meditation.english_jft import EnglishJft
from fetch_meditation.german_jft import GermanJft
from fetch_meditation.jft import Jft
from fetch_meditation.jft_settings import JftSettings
from fetch_meditation.jft_language import JftLanguage


@pytest.fixture
def english_jft_settings():
    return JftSettings(JftLanguage.English)


@pytest.fixture
def german_jft_settings():
    return JftSettings(JftLanguage.German)


def test_jft_language_property(english_jft_settings, german_jft_settings):
    english_jft = Jft(english_jft_settings)
    german_jft = Jft(german_jft_settings)

    assert english_jft.language == JftLanguage.English
    assert german_jft.language == JftLanguage.German


def test_get_instance(english_jft_settings, german_jft_settings):
    english_jft = Jft.get_instance(english_jft_settings)
    german_jft = Jft.get_instance(german_jft_settings)

    assert isinstance(english_jft, EnglishJft)
    assert isinstance(german_jft, GermanJft)
