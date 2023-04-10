import threading
import tkinter as tk
import wave
import os
from functions import transcribe

import pyaudio


class AudioPlayer:
    # Define constants for audio recording
    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    def __init__(self, records_dir: str = "records"):
        self.records_dir = records_dir
        # Initialize the player
        master = tk.Tk()
        master.title("Audio Player")
        master.geometry("400x200")

        # Initialize the audio player
        self.is_recording = False
        self.is_playing = False
        self.master = master
        self.audio = pyaudio.PyAudio()

        # Create Objects in the player
        self.label = tk.Label(master, text="File Name:")
        self.label.pack(pady=10)

        self.input_box = tk.Entry(master, width=50)
        self.input_box.insert(0, "audio")
        self.input_box.pack(pady=10)

        self.record_button = tk.Button(master, text="Record", command=self.start_recording)
        self.stop_record_button = tk.Button(master, text="Stop Record", command=self.stop_recording)

        self.play_button = tk.Button(master, text="Play", command=self.start_playing)
        self.stop_play_button = tk.Button(master, text="Stop Play", command=self.stop_audio)

        self.infer_button = tk.Button(master, text="Infer", command=self.infer_audio)

        self.exit_button = tk.Button(master, text="Exit", command=self.exit)

        # Create the layout
        top_frame = tk.Frame(master)
        middle_frame = tk.Frame(master)
        bottom_frame = tk.Frame(master)

        # add buttons to frames
        self.record_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_record_button.pack(side=tk.LEFT, padx=10, pady=10)
        top_frame.pack()

        self.play_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.stop_play_button.pack(side=tk.LEFT, padx=10, pady=10)
        middle_frame.pack()

        self.infer_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.exit_button.pack(side=tk.LEFT, padx=10, pady=10)
        bottom_frame.pack()

    def start_playing(self):
        # Start recording on a separate thread
        t = threading.Thread(target=self.play_audio)
        t.start()

    def play_audio(self):
        self.is_playing = True
        # Get the file name
        file_name = self.input_box.get() + ".wav"
        file_path = os.path.join(self.records_dir, file_name)

        # Play the audio file
        wave_file = wave.open(file_path, "rb")
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                 output=True)
        data = wave_file.readframes(self.CHUNK_SIZE)
        while data and self.is_playing:
            stream.write(data)
            data = wave_file.readframes(self.CHUNK_SIZE)

        self.is_playing = False
        stream.stop_stream()
        stream.close()

    def stop_audio(self):
        # Stop playing
        self.is_playing = False

    def start_recording(self):
        # Start recording on a separate thread
        t = threading.Thread(target=self.record_audio)
        t.start()

    def record_audio(self):
        self.is_recording = True

        # Create an input stream with the desired sample rate, format, and number of channels
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
                                 input=True, frames_per_buffer=self.CHUNK_SIZE)

        print("Recording started")
        frames = []
        while self.is_recording:
            # Capture a block of audio data from the stream
            data = stream.read(self.CHUNK_SIZE)
            frames.append(data)

        print("Recording stopped")

        # Stop and close the input stream and PyAudio object
        stream.stop_stream()
        stream.close()

        # Save the audio data as a WAV file
        file_name = self.input_box.get() + ".wav"
        file_path = os.path.join(self.records_dir, file_name)
        wave_file = wave.open(file_path, 'wb')
        wave_file.setnchannels(self.CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wave_file.setframerate(self.RATE)
        wave_file.writeframes(b''.join(frames))
        wave_file.close()

        print("WAV file saved...")

    def stop_recording(self):
        # Stop recording
        self.is_recording = False

    def infer_audio(self):
        file_name = self.input_box.get() + ".wav"
        file_path = os.path.join(self.records_dir, file_name)
        transcribe(file_path)

    def exit(self):
        self.audio.terminate()
        self.master.destroy()

    def start(self):
        self.master.mainloop()
