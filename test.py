from fetch_meditation.jft_language import JftLanguage
from fetch_meditation.jft_settings import JftSettings
from fetch_meditation.jft import Jft

from fetch_meditation.spad_language import SpadLanguage
from fetch_meditation.spad_settings import SpadSettings
from fetch_meditation.spad import Spad


# settings = JFTSettings(JFTLanguage.English)
# jft_instance = JFT.get_instance(settings)
# jft_entry = jft_instance.fetch()
# lang_name = jft_instance.get_language()
# print(jft_entry.without_tags())


for language in JftLanguage:
    print(f"\n\n-=-=-=-=-=-=-=-= JFT - {language} -=-=-=-=-=-=-=-=\n\n")
    settings = JftSettings(language)
    jft_instance = Jft.get_instance(settings)
    jft_entry = jft_instance.fetch()
    lang_name = settings.language
    print(jft_entry.quote)
    print(f" -- {lang_name}")


for language in SpadLanguage:
    print(f"\n\n-=-=-=-=-=-=-=-= SPAD - {language} -=-=-=-=-=-=-=-=\n\n")
    settings = SpadSettings(language)
    spad_instance = Spad.get_instance(settings)
    spad_entry = spad_instance.fetch()
    lang_name = settings.language
    print(spad_entry.quote)
    print(f" -- {lang_name}")
