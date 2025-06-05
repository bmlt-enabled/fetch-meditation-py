from fetch_meditation.jft_language import JftLanguage
from fetch_meditation.jft_settings import JftSettings
from fetch_meditation.english_jft import EnglishJft

# Test with a timezone
settings = JftSettings(language=JftLanguage.English, time_zone="Australia/Sydney")
jft = EnglishJft(settings)
entry = jft.fetch()

# Print the date, which should reflect the Sydney timezone
print(f"Date from JFT with Sydney timezone: {entry.date}")
