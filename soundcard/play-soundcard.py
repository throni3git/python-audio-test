import numpy as np
import soundcard as sc
import soundfile as sf

import utils

if __name__ == "__main__":

    cli_args = utils.get_CLI_args()

    try:
        data, fs = sf.read(cli_args.wavefile_name, dtype=np.float32)

        block_size = 256
        print(f"Framerate: {fs}")

        spk = sc.default_speaker()
        print(spk)
        with spk.player(samplerate=fs, blocksize=block_size) as sp:
            # print(sp.buffersize)
            sp.latency
            while True:
                sp.play(data)

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
