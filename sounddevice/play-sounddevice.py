import argparse
import sys

import numpy as np
import sounddevice as sd
import soundfile as sf


if __name__ == "__main__":

    parser = argparse.ArgumentParser("play wavefile")
    parser.add_argument('wavefile_name', default="examples/click.wav",
                        type=str, nargs='?', help='use this file to play')
    args = parser.parse_args()

    try:
        data, fs = sf.read(args.wavefile_name, dtype=np.float32)

        print(f"Framerate: {fs}")

        sd.play(data, fs)
        status = sd.wait()
    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
    if status:
        parser.exit('Error during playback: ' + str(status))
