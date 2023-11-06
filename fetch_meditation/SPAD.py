from typing import Dict, List, Any
from fetch_meditation.spad_language import SpadLanguage
from fetch_meditation.english_spad import EnglishSpad


class Spad:
    def __init__(self, settings: Any) -> None:
        self.settings = settings

    def fetch(self) -> None:
        pass

    @property
    def language(self) -> SpadLanguage:
        return self.settings.language

    @staticmethod
    def get_instance(settings: Any) -> EnglishSpad:
        return {
            SpadLanguage.English: EnglishSpad,
        }[settings.language](settings)
