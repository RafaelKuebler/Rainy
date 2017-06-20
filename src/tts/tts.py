import os
import uuid
import pyglet
from gtts import gTTS
from time import sleep

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

    def __init__(self, audio_folder, language='en', slow=False):
        """Save relevant data for converter

        Args:
            language (string): language code for desired language
            slow (bool): whether the speech should be slower than default
        """
        self.language = language
        self.slow = slow

        self._audio_dir = audio_folder
        if not os.path.exists(self._audio_dir):
            os.makedirs(self._audio_dir)

    def say(self, text):
        audio_file_name = "{}.mp3".format(uuid.uuid4())
        audio_path = os.path.join(self._audio_dir, audio_file_name)

        speech = gTTS(text=str(text), lang=self.language, slow=self.slow)
        speech.save(audio_path)
        # print("Audio \'{}\' saved to: {}".format(text, audio_file_name))

        music = pyglet.media.load(audio_path, streaming=False)
        music.play()
        # print("Playing audio file: {}".format(audio_file_name))

        sleep(music.duration)  # prevent from killing
        # print("Finished playing: {}".format(audio_file_name))

        os.remove(audio_path)
        # print("Deleted: {}".format(audio_file_name))
