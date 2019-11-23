import wave
import time
import pyaudio
import io
import concurrent.futures
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import gtts
from io import BytesIO
from tolkien import Tolkien

corpus = "   ______                           \n  / ____/___  _________  __  _______\n / /   / __ \\/ ___/ __ \\/ / / / ___/\n/ /___/ /_/ / /  / /_/ / /_/ (__  ) \n\\____/\\____/_/  / .___/\\__,_/____/  \n               /_/                  "

class Parlay:
    def __init__(self, lang = 'no'):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        # a list containing the recorded audio files, acting as a queue.
        self.audio_queue = []
        self.recognize_queue = []
        self.action_queue = []
        self.tolk = Tolkien()

        # Variable used with the threading functions
        self.recognized_text = ""

        try:
            if gtts.lang.tts_langs()[lang]:
                self.language = lang
        except KeyError:
            print("Invalid language code")

    def calibrate_recognizer(self):
        self.recognizer.energy_threshold = 150 # Energy threshold sets the threshold for when audio is considered speech.
        self.recognizer.pause_threshold = 0.5 # Sets the number of seconds that determines if a spoken phrase is considered complete.
        self.recognizer.non_speaking_duration = 0.5 # Sets the number of seconds of non-speaking audio to keep on both sides of recording.
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)

    def listen(self, time_limit = None, timeout = None):
        with self.mic as source:
            try:
                # Returns 1 to signal that the function ``speech_recognition.listen()`` did not time out,
                # and an instance of AudioData from SpeechRecognition which can be passed to ``recognize``
                audio = self.recognizer.listen(source, timeout = timeout, phrase_time_limit = time_limit)
                self.audio_queue.append(audio)
            except sr.WaitTimeoutError:
                # Returns 0 to signal that the function ``speech_recognition.listen()`` did time out
                pass

    def thr_listen(self, time_limit = None, timeout = None):
        with self.mic as source:
            try:
                # Returns 1 to signal that the function ``speech_recognition.listen()`` did not time out,
                # and an instance of AudioData from SpeechRecognition which can be passed to ``recognize``
                audio = self.recognizer.listen(source, timeout = timeout, phrase_time_limit = time_limit)
                # action_list.append([0, time_limit, timeout])
                self.recognize_queue.append(audio)
            except sr.WaitTimeoutError:
                pass
                # Pass if ``speech_recognition.listen()`` timed out
                # action_list.append([0, time_limit, timeout])

    def thr_recognize(self, audio):
        print("Recognize")
        try:
            # ``speech_recognition.recognize_google()`` takes a key as an optional parameter. It uses a default key if none is given.
            string_of_text = self.recognizer.recognize_google(audio, language = self.language)
            print("Tolk")
            self.tolk.extract_commands(string_of_text)
            self.action_queue.append([2, self.tolk.stringify_commands()])
        except sr.UnknownValueError:
            pass
            # print("Jeg forstod ikke det.")
            # action_list.append(["phrase", "Google Speech Recognition does not understand what you said."])
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            # action_list.append(["phrase", "Could not request results from Google Speech Recognition service; {0}".format(e)])
        except IndexError:
            print("Ingen data.")
            # action_list.append(["phrase", "No audio data to recognize."])

    def recognize(self):
        try:
            # ``speech_recognition.recognize_google()`` takes a key as an optional parameter. It uses a default key if none is given.
            string_of_text = self.recognizer.recognize_google(self.audio_queue[0], language = self.language)
            self.audio_queue.pop(0)
            return string_of_text
        except sr.UnknownValueError:
            return "Google Speech Recognition does not understand what you said."
        except sr.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)
        except IndexError:
            return "No audio data to recognize."

    def speak(self, text):
        output_file_object = BytesIO()
        tts = gtts.gTTS(text, self.language)
        tts.write_to_fp(output_file_object)
        output_file_object.seek(0)
        output_audio = AudioSegment.from_file(output_file_object, format = 'mp3')
        play(output_audio)

    def run(self, time_limit = None, timeout = None):
        self.calibrate_recognizer()
        with concurrent.futures.ThreadPoolExecutor(max_workers = 20) as executor:
            print(corpus)
            listen_thread = executor.submit(self.thr_listen(time_limit, timeout))
            while True:
                if listen_thread.done():
                    listen_thread = executor.submit(self.thr_listen(time_limit, timeout))
                if self.recognize_queue:
                    executor.map(self.thr_recognize, self.recognize_queue)
                    self.recognize_queue = []
                if self.action_queue:
                    action = self.action_queue.pop(0)
                    if action[1]:
                        print("Kommando :" + action[1])
