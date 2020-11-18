import sounddevice as sd
import numpy as np
from pprint import pprint


def print_all_devices() -> None:
    print(f"PortAudio version {sd.get_portaudio_version()}")

    hostapis = sd.query_hostapis()
    print(hostapis)

    devices = sd.query_devices()
    print(devices)

    print("default output")
    spk_all = sd.query_devices(kind="output")
    pprint(spk_all)

    print("default input")
    mic_all = sd.query_devices(kind="input")
    pprint(mic_all)

    while True:
        choose = input()
        choose = int(choose)
        pprint(sd.query_devices(choose))


if __name__ == "__main__":
    print_all_devices()
