
import pyaudio


def print_details(device) -> None:
    ha = p.get_host_api_info_by_index(device['hostApi'])["name"]
    ins = device['maxInputChannels']
    outs = device['maxOutputChannels']
    sr = device["defaultSampleRate"]
    lat_in_hi = device["defaultHighInputLatency"]
    lat_in_lo = device["defaultLowInputLatency"]
    lat_out_hi = device["defaultHighOutputLatency"]
    lat_out_lo = device["defaultLowOutputLatency"]
    print(f"{device['index']:2d} {device['name']}, {ha} ({ins} in, {outs} out), default samplerate {sr}, latency in({lat_in_lo:.3f}-{lat_in_hi:.3f}) out({lat_out_lo:.3f}-{lat_out_hi:.3f})")


def print_all_devices() -> None:

    print("PyAudio Devices:")
    for idx in range(p.get_device_count()):
        dev = p.get_device_info_by_index(idx)
        print_details(dev)

        # prefix = "*" if str(mic) == str(mic_default) else " "
        # print(f"{prefix} {mic.name}       id: {mic.id}")


if __name__ == "__main__":
    p = pyaudio.PyAudio()

    print_all_devices()
