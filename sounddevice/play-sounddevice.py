import argparse
import sys

import numpy as np
import sounddevice as sd
import soundfile as sf

CHUNK = 1024


if __name__ == "__main__":

    parser = argparse.ArgumentParser("play wavefile")
    parser.add_argument('wavefile_name', type=str, nargs='?', help='use this file to play')
    args = parser.parse_args()

    try:
        fn = "examples/click.wav"
        if args.wavefile_name is not None:
            fn = args.wavefile_name
        data, fs = sf.read(fn, dtype=np.float32)

        print(f"Framerate: {fs}")

        sd.play(data, fs)
        status = sd.wait()
    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
    if status:
        parser.exit('Error during playback: ' + str(status))
