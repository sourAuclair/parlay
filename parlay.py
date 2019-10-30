import wave
import time
import pyaudio
import io
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import gtts
from io import BytesIO

class Parlay:
    def __init__(self, lang = 'no'):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        try:
            if gtts.lang.tts_langs()[lang]:
                self.language = lang
        except KeyError:
            print("Invalid language code")

    def calibrate_recognizer(self):
        self.recognizer.energy_threshold = 70 # Energy threshold sets the threshold for when audio is considered speech.
        self.recognizer.pause_threshold = 1 # Sets the number of seconds that determines if a spoken phrase is considered complete.
        self.recognizer.non_speaking_duration = 0.5 # Sets the number of seconds of non-speaking audio to keep on both sides of recording.
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self, time_limit = None, timeout = None):
        with self.mic as source:
            try:
                # Returns 1 to signal that the function ``speech_recognition.listen()`` did not time out,
                # and an instance of AudioData from SpeechRecognition which can be passed to ``recognize``
                return [1, self.recognizer.listen(source, timeout = timeout, phrase_time_limit = time_limit)]
            except sr.WaitTimeoutError:
                # Returns 0 to signal that the function ``speech_recognition.listen()`` did time out,
                # and a descriptive string.
                return [0, "Timeout while waiting for sound"]


    def recognize(self, audio_data):
        try:
            # ``speech_recognition.recognize_google()`` takes a key as an optional parameter. It uses a default key if none is given.
            return self.recognizer.recognize_google(audio_data, language = self.language) # Returns a string containing the spoken phrase given as audio_data
        except sr.UnknownValueError:
            return "Google Speech Recognition does not understand what you said."
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

    def speak(self, text):
        output_file_object = BytesIO()
        tts = gtts.gTTS(text, self.language)
        tts.write_to_fp(output_file_object)
        output_file_object.seek(0)
        output_audio = AudioSegment.from_file(output_file_object, format = 'mp3')
        play(output_audio)
