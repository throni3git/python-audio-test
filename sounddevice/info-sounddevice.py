import sounddevice as sd
import numpy as np


def print_details(device) -> None:
    hostapi_names = [hostapi['name'] for hostapi in sd.query_hostapis()]
    ha = hostapi_names[device['hostapi']]
    ins = device['max_input_channels']
    outs = device['max_output_channels']
    lat_in_hi = device["default_high_input_latency"]
    lat_in_lo = device["default_low_input_latency"]
    lat_out_hi = device["default_high_output_latency"]
    lat_out_lo = device["default_low_output_latency"]
    print(f"{device['name']}, {ha} ({ins} in, {outs} out), latency in({lat_in_lo:.3f}-{lat_in_hi:.3f}) out({lat_out_lo:.3f}-{lat_out_hi:.3f})")


def print_all_devices() -> None:
    print(f"PortAudio version {sd.get_portaudio_version()}")

    hostapis = sd.query_hostapis()
    print(hostapis)

    devices = sd.query_devices()
    print(devices)

    # default output
    spk_all = sd.query_devices(kind="output")
    print_details(spk_all)

    # default input
    mic_all = sd.query_devices(kind="input")
    print_details(mic_all)

    while True:
        choose = input("Interested in a particular device? Which one? ")
        choose = int(choose)
        print_details(sd.query_devices(choose))


if __name__ == "__main__":
    print_all_devices()
