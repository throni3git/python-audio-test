import argparse
from pprint import pprint
import sys
import time
import wave

import pyaudio


def callback(in_data, frame_count, time_info, status):
    # print(frame_count)
    data = wf.readframes(frame_count)
    # print(data)
    return (data, pyaudio.paContinue)


if __name__ == "__main__":

    parser = argparse.ArgumentParser("play wavefile")
    parser.add_argument('wavefile_name', default="examples/click.wav",
                        type=str, nargs='?', help='use this file to play')
    args = parser.parse_args()

    wf = wave.open(args.wavefile_name, 'rb')

    framerate = wf.getframerate()
    print(f"Framerate: {framerate}")
    sample_width = wf.getsampwidth()
    print(f"Sample width: {sample_width}")

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    pa_format = p.get_format_from_width(sample_width)
    print(f"PyAudio Format: {pa_format}")

    pprint(p.get_host_api_info_by_index(0))
    pprint(p.get_default_output_device_info())
    pprint(p.get_default_input_device_info())

    # open stream using callback (3)
    stream = p.open(format=pa_format,
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    frames_per_buffer=64,
                    stream_callback=callback)

    print(f"Stream output latency: {stream.get_output_latency()}")

    # start the stream (4)
    stream.start_stream()

    # wait for stream to finish (5)
    while stream.is_active():
        time.sleep(0.1)

    # stop stream (6)
    stream.stop_stream()
    stream.close()
    wf.close()

    # close PyAudio (7)
    p.terminate()
