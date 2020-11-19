import argparse

import numpy as np
import soundcard as sc
import soundfile as sf

if __name__ == "__main__":

    parser = argparse.ArgumentParser("play wavefile")
    parser.add_argument('wavefile_name', default="examples/click.wav",
                        type=str, nargs='?', help='use this file to play')
    args = parser.parse_args()

    try:
        data, fs = sf.read(args.wavefile_name, dtype=np.float32)

        block_size = 256
        print(f"Framerate: {fs}")

        spk = sc.default_speaker()
        print(spk)
        with spk.player(samplerate=fs, blocksize=block_size) as sp:
            # print(sp.buffersize)
            while True:
                sp.play(data)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
