import whisper
from openai import OpenAI
import timeit

def transcribe(audio_path, model_name="base.en"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result["text"]

def transcribe_timeit(audio_path, model_name="base.en"):

    model = whisper.load_model(model_name)

    def transcribe_code():
        _ = model.transcribe(audio_path)

    n = 10
    execution_time = timeit.timeit(stmt=transcribe_code, number=n) / n
    return execution_time


def transcribe_api(audio_path):
    client = OpenAI()

    audio_file = open(audio_path, "rb")

    # timeit

    result = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    print(result.text)


def transcribe_api_timeit(audio_path, model_name="base.en"):

    setup_code = """
    client = OpenAI()
    audio_file = open(audio_path, "rb")
    """
    code = """
result = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
    )
"""
    n = 10
    execution_time = timeit.timeit(stmt=code, globals=globals(), setup=setup_code, number=n) / n
    return execution_time