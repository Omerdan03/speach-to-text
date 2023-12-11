import whisper
from openai import OpenAI
import timeit

def transcribe(audio_path):
    model = whisper.load_model("base.en")
    result = model.transcribe(audio_path)
    print(result["text"])

def transcribe_timeit(audio_path):
    model = whisper.load_model("base.en")

    code_to_measure = """result = model.transcribe(audio_path)"""

    execution_time = timeit.timeit(stmt=code_to_measure, globals=globals(), number=10)
    print(execution_time)


def transcribe_api(audio_path):
    client = OpenAI()

    audio_file = open(audio_path, "rb")

    # timeit

    result = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    print(result.text)


def transcribe_api_timeit(audio_path):

    client = OpenAI()
    audio_file = open(audio_path, "rb")

    code_to_measure = """
result = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
    )
"""

    execution_time = timeit.timeit(stmt=code_to_measure, globals=globals(), number=10)
    print(execution_time)