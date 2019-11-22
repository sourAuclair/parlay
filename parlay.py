import wave
import time
import pyaudio
import io
import threading
import concurrent.futures
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import gtts
from io import BytesIO
from tolkien import Tolkien
import concurrent.futures

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
                return 1
            except sr.WaitTimeoutError:
                # Returns 0 to signal that the function ``speech_recognition.listen()`` did time out
                return 0

    def thr_listen(self, action_list, time_limit = None, timeout = None):
        with self.mic as source:
            try:
                # Returns 1 to signal that the function ``speech_recognition.listen()`` did not time out,
                # and an instance of AudioData from SpeechRecognition which can be passed to ``recognize``
                audio = self.recognizer.listen(source, timeout = timeout, phrase_time_limit = time_limit)
                # action_list.append([0, time_limit, timeout])
                action_list.append([3, audio])
            except sr.WaitTimeoutError:
                pass
                # Pass if ``speech_recognition.listen()`` timed out
                # action_list.append([0, time_limit, timeout])


    # NOT IN USE. CONSIDER DELETING.
    def listen_in_background(self, time_limit = None, timeout = 1):
        """
        Spawns a thread to repeatedly record phrases from ``source`` (an ``AudioSource`` instance) into an ``AudioData`` instance and call ``callback`` with that ``AudioData`` instance as soon as each phrase are detected.

        Returns a function object that, when called, requests that the background listener thread stop. The background thread is a daemon and will not stop the program from exiting if there are no other non-daemon threads. The function accepts one parameter, ``wait_for_stop``: if truthy, the function will wait for the background listener to stop before returning, otherwise it will return immediately and the background listener thread might still be running for a second or two afterwards. Additionally, if you are using a truthy value for ``wait_for_stop``, you must call the function from the same thread you originally called ``listen_in_background`` from.

        Phrase recognition uses the exact same mechanism as ``recognizer_instance.listen(source)``. The ``phrase_time_limit`` parameter works in the same way as the ``phrase_time_limit`` parameter for ``recognizer_instance.listen(source)``, as well.

        The ``callback`` parameter is a function that should accept two parameters - the ``recognizer_instance``, and an ``AudioData`` instance representing the captured audio. Note that ``callback`` function will be called from a non-main thread.
        """
        
        running = [True]

        def threaded_listen():
            while running[0]:
                try:  # listen for 1 second, then check again if the stop function has been called
                    print("Listening")
                    [ret_code, audio] = self.listen(time_limit, timeout)
                except sr.WaitTimeoutError:  # listening timed out, just try again
                    pass
                else:
                    print("TEST: running = ", running[0])
                    if running[0] and ret_code == 1: print(self.recognize(audio))

        def stopper(wait_for_stop=True):
            print("STOPPER")
            running[0] = False
            if wait_for_stop:
                listener_thread.join()  # block until the background thread is done, which can take around 1 second

        listener_thread = threading.Thread(target=threaded_listen)
        listener_thread.daemon = True
        listener_thread.start()
        return stopper


    # NOT IN USE. UNDER DEVELOPMENT
    def continously_listen(self, time_limit = None, timeout = None):
        # listen_thread = threading.Thread(target = self.listen(timeout = 1))
        # listen_thread.daemon = True
        # recognize_thread = threading.Thread(target = self.recognize())
        # recognize_thread.daemon = True
        # listen_thread.start()
        # while True:
        #     if self.audio_queue:
        #         recognize_thread.start()
        #         listen_thread.start()
        #         recognize_thread.join()
        #     else:
        #         time.sleep(0.1)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            # Initialize listening
            listen = executor.submit(self.listen(time_limit, timeout))
            while True:
                # Listening thread is not done and no audiodata is in the queue
                if not (listen.done() or self.audio_queue):
                    continue
                # Listening thread is done but no audiodata is in the queue
                elif listen.done() and not self.audio_queue:
                    print("Listening thread is done")
                    listen = executor.submit(self.listen, time_limit, timeout)
                # Listening thread is done and there is audiodata in the queue
                elif listen.done() and self.audio_queue:
                    print("Listening thread is done")
                    # print("Recognizing")
                    listen = executor.submit(self.listen, time_limit, timeout)
                    recognize = executor.submit(self.thr_recognize)
                    # print(recognize.result())
                # Listening thread is not done but there is audiodata in the queue
                elif not listen.done() and self.audio_queue:
                    # print("Recognizing")
                    recognize = executor.submit(self.thr_recognize)
                    # print(recognize.result())
                else:
                    time.sleep(0.5)
                # Checking if the recognizer thread has finished
                if len(self.recognized_text) > 0:
                    print(self.recognized_text)
        
    def thr_recognize(self, action_list, audio):
        try:
            # ``speech_recognition.recognize_google()`` takes a key as an optional parameter. It uses a default key if none is given.
            string_of_text = self.recognizer.recognize_google(audio, language = self.language)
            print("tolk")
            self.tolk.extract_commands(string_of_text)
            action_list.insert(0, [2, self.tolk.stringify_commands()])
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
        print(corpus)
        self.calibrate_recognizer()
        with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
            print("power on")
            listen_thread = executor.submit(self.thr_listen(self.action_queue, time_limit, timeout))
            while True:
                if listen_thread.done():
                    listen_thread = executor.submit(self.thr_listen(self.action_queue, time_limit, timeout))
                if self.action_queue:
                    action = self.action_queue.pop(0)
                    # TOLK
                    if action[0] == 1:
                        print("tolk")
                        tolk_thread = executor.submit(self.tolk.thr_extract_commands(self.action_queue, action[1]))
                    # PHRASE
                    elif action[0] == 2:
                        print("kommando: " + action[1])
                    # RECOGNIZE
                    elif action[0] == 3:
                        print("recognize")
                        recognize_thread = executor.submit(self.thr_recognize(self.action_queue, action[1]))







