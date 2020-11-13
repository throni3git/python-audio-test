import argparse
import sys
import wave

import pyaudio

CHUNK = 1024


if __name__ == "__main__":

    parser = argparse.ArgumentParser("play wavefile")
    parser.add_argument('wavefile_name', type=str, nargs='?', help='use this file to play')
    args = parser.parse_args()

    fn = "examples/click.wav"
    if args.wavefile_name is not None:
        fn = args.wavefile_name
    wf = wave.open(fn, 'rb')

    framerate = wf.getframerate()
    print(f"Framerate: {framerate}")
    sample_width = wf.getsampwidth()
    print(f"Sample width: {sample_width}")

    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    pa_format = p.get_format_from_width(sample_width)
    print(f"PyAudio Format: {pa_format}")

    # open stream (2)
    stream = p.open(format=pa_format,
                    channels=wf.getnchannels(),
                    rate=framerate,
                    output=True)

    print(f"Stream output latency: {stream.get_output_latency()}")

    # read data
    data = wf.readframes(CHUNK)

    # play stream (3)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # stop stream (4)
    stream.stop_stream()
    stream.close()

    # close PyAudio (5)
    p.terminate()
