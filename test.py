from fetch_meditation.JFTLanguage import JFTLanguage
from fetch_meditation.JFTSettings import JFTSettings
from fetch_meditation.JFT import JFT

from fetch_meditation.SPADLanguage import SPADLanguage
from fetch_meditation.SPADSettings import SPADSettings
from fetch_meditation.SPAD import SPAD


# settings = JFTSettings(JFTLanguage.English)
# jft_instance = JFT.get_instance(settings)
# jft_entry = jft_instance.fetch()
# lang_name = jft_instance.get_language()
# print(jft_entry.to_json())


for language in JFTLanguage:
    print(f"\n\n-=-=-=-=-=-=-=-= JFT - {language} -=-=-=-=-=-=-=-=\n\n")
    settings = JFTSettings(language)
    jft_instance = JFT.get_instance(settings)
    jft_entry = jft_instance.fetch()
    lang_name = jft_instance.get_language()
    print(jft_entry.quote)
    print(f" -- {lang_name}")


for language in SPADLanguage:
    print(f"\n\n-=-=-=-=-=-=-=-= SPAD - {language} -=-=-=-=-=-=-=-=\n\n")
    settings = SPADSettings(language)
    spad_instance = SPAD.get_instance(settings)
    spad_entry = spad_instance.fetch()
    lang_name = spad_instance.get_language()
    print(spad_entry.quote)
    print(f" -- {lang_name}")
