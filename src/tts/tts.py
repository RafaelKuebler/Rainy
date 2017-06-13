from gtts import gTTS
import urllib3
urllib3.disable_warnings()

'''
Interesting language codes:
    'en' : 'English'
    'de' : 'German'
    'es' : 'Spanish' / 'es-es' : 'Spanish (Spain)' ?
'''


class TTSConverter:
    """Convert text to speech using the Google Text-to-Speech-API.

    Attributes:
        language (string): language code for desired language
        slow (bool): whether the speech should be slower than default
    """

    def __init__(self, language='en', slow=True):
        """Save relevant data for converter

        Args:
            language (string): language code for desired language
            slow (bool): whether the speech should be slower than default
        """
        self.language = language
        self.slow = slow

    def say(self, text):
        speech = gTTS(text=text, lang=self.language, slow=self.slow)
        speech.save("rainy.mp3")

        # play what is saved in "rainy.mp3"
