import wave
import time
import pyaudio
import io
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import gtts
from io import BytesIO

def explicit():
	from google.oauth2 import service_account

	return service_account.Credentials.from_service_account_file('C:/Users/Johan/Documents/GCloud/Cogitron-3673ea643ce9.json')

def synthesize(text, credential):
	print("Synthesizing")
	out_file = 'output.mp3'
	from google.cloud import texttospeech
	client = texttospeech.TextToSpeechClient(credentials = credential)

	input_text = texttospeech.types.SynthesisInput(text=text)

	voice = texttospeech.types.VoiceSelectionParams(
		language_code = 'no-NO',
		ssml_gender = texttospeech.enums.SsmlVoiceGender.MALE)

	audio_config = texttospeech.types.AudioConfig(
		audio_encoding = texttospeech.enums.AudioEncoding.MP3)

	response = client.synthesize_speech(input_text, voice, audio_config)

	with open(out_file, 'wb') as out:
		out.write(response.audio_content)
		print("Done synthesizing")
	return out_file

with open('C:/Users/Johan/Documents/GCloud/Cogitron-3673ea643ce9.json', 'r') as file:
	credential = file.read()

while True:
	text = ''
	r = sr.Recognizer()
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print("Say something")
		audio = r.listen(source)

		try:
			text = r.recognize_google_cloud(audio, credentials_json = credential, language = "no-NO")
		except sr.UnknownValueError:
			print("I did not understand that.")
		except sr.RequestError as e:
			print("Request error {0}".format(e))

		if text:
			audio_file = synthesize(text, credential)
			audio = AudioSegment.from_mp3(audio_file)
			play(audio)

