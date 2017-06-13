#!/usr/bin/env python

from gtts import gTTS

'''
Interesting language codes:
    'en' : 'English'
    'de' : 'German'
    'es' : 'Spanish' / 'es-es' : 'Spanish (Spain)' ?
'''
tts = gTTS(text='Hello', lang='en', slow=True)