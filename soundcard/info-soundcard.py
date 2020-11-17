import soundcard as sc
import numpy as np


def print_all_devices() -> None:
    print("speakers")
    spk_all = sc.all_speakers()
    spk_default = sc.default_speaker()
    for spk in spk_all:
        prefix = "*" if str(spk) == str(spk_default) else " "
        print(f"{prefix} {spk.name}       id: {spk.id}")

    print("microphones")
    mic_all = sc.all_microphones()
    mic_default = sc.default_microphone()
    for mic in mic_all:
        prefix = "*" if str(mic) == str(mic_default) else " "
        print(f"{prefix} {mic.name}       id: {mic.id}")


if __name__ == "__main__":
    print_all_devices()
