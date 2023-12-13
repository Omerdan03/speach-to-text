from recorder import AudioPlayer


def main():
    my_audio_player = AudioPlayer(engine="whisper")
    my_audio_player.start()


if __name__ == "__main__":
    main()
