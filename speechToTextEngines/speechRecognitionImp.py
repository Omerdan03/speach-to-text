import timeit

import speech_recognition as sr


# Initialize the recognizer
recognizer = sr.Recognizer()
N=10

def read_audio(audio_path: str):
	# Load the audio file
	with sr.AudioFile(audio_path) as source:
		# Adjust for ambient noise
		recognizer.adjust_for_ambient_noise(source)

		# Record the audio from the file
		audio = recognizer.record(source)

	return audio


def transcribe(audio_path):
	# Load the audio file
	audio = read_audio(audio_path)
	try:
		# Use the recognizer to perform speech recognition
		# return recognizer.recognize_sphinx(audio)
		# return recognizer.recognize_google_cloud(audio)  # requires key
		# return recognizer.recognize_wit(audio)  # requires key
		# return recognizer.recognize_azure(audio)  # requires key
		# return recognizer.recognize_bing(audio)  # requires key
		# return recognizer.recognize_lex(audio)  # requires key
		# return recognizer.recognize_houndify(audio)  # requires key
		# return recognizer.recognize_amazon(audio)
		# return recognizer.recognize_assemblyai(audio)  # requires key
		# return recognizer.recognize_ibm(audio)  # requires key
		# return recognizer.recognize_tensorflow(audio)
		return recognizer.recognize_whisper(audio)
		# return recognizer.recognize_vosk(audio)
		# return recognizer.recognize_google(audio)
		# return recognizer.recognize_whisper_api(audio)
		# return recognizer.recognize_api(audio)

	except sr.UnknownValueError:
		print("Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))


def transcribe_timeit(audio_path):
	audio = read_audio(audio_path)

	def transcribe_code():
		_ = recognizer.recognize_whisper(audio)

	execution_time = timeit.timeit(stmt=transcribe_code, number=N) / N
	return execution_time
