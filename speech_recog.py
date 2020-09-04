from datetime import datetime, timedelta
from inspect import signature
import time
import speech_recognition as sr
import get_requirements as svw

# Quickly make sure pyaudio is installed
try:
    import pyaudio
except ModuleNotFoundError:
    svw.get_pyaudio()

def _normalizeString(s):
    return ''.join(e for e in s if e.isalnum()).lower()

def _getSoundMixer():
    svw.download()
    svw.enable('Stereo Mixer')
    
    # Scan all inputs for stereo mix
    inputs = list(map(_normalizeString,sr.Microphone.list_microphone_names()))
    for i in inputs:
        if 'stereomix' in i:
            try:
                device_index = inputs.index(i)
                # Check if it works
                with sr.Microphone(device_index=device_index):
                    pass
                break
            except OSError:
                device_index = None
    return device_index

class Listener():
    """Listens to the loopback audio device. Currently only compatible with certain Windows machines"""

    def __init__(self):
        self._listening = False
        self.heard = ""
        self.lasttime = datetime.now()
        # Instantiate and calibrate mic
        self.r = sr.Recognizer()
        self.r.energy_threshold = 45.1
        self.r.pause_threshold = 0.5
        self.mic = sr.Microphone(device_index=_getSoundMixer())
    
    def set_on_hear(self, function):
        """Sets the loopback function. Not required to start listening. Callback must have exactly 1 string argument"""
        assert len(signature(function).parameters) == 1
        self._callback_func = function
    
    def start_listening(self):
        """Begins listening"""
        def recog_callback(recognizer, audio):
            try:
                text = recognizer.recognize_google(audio)
                self.lasttime = datetime.now()
                self.heard = str(self.heard) + str(text) + '\n'
                if self._callback_func:
                    self._callback_func(text)
            except (sr.UnknownValueError, sr.RequestError): 
                pass # Ignore errors for now
        
        # Now start listening
        self._stop_listening = self.r.listen_in_background(self.mic, recog_callback)
        self.lasttime = datetime.now()
        self._listening = True

    def stop_listening(self, wait_for_stop=True):
        """Stops listening"""
        if self._stop_listening:
            self._stop_listening(wait_for_stop=wait_for_stop)
            self._listening = False
    
    def listen(self, stop_timer=timedelta(0,30)):
        """Halts the main thread until no new audio was recognized for 'stop_timer'. 
        'stop_timer' can be either a timedelta or a number of seconds"""
        
        if not self._listening: return
        if isinstance(stop_timer, timedelta): stop_timer = stop_timer.total_seconds()
        while (datetime.now() - self.lasttime).total_seconds() < stop_timer:
            time.sleep(0.1)
