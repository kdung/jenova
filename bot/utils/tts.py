"""TTS utility"""

import logging

import app

from framework.tts import PyttsxEngine
from framework.tts import EV3TTSEngine
from framework.tts import OSXTTSEngine

def say(engine_name, texts):
    """Speak texts with a specified engine"""
    osx_voice = app.get_config('engine.voices.osx')
    tts_engines = {
        'pyttsx': PyttsxEngine(),
        'ev3': EV3TTSEngine(),
        'osx': OSXTTSEngine(osx_voice)
    }
    engine = tts_engines.get(engine_name)
    if engine is None:
        logging.warning('engine not configured: ' + engine_name)
        return
    engine.say(texts)