import numpy as np
import sounddevice as sd
import soundfile as sf

import utils

if __name__ == "__main__":

    cli_args = utils.get_CLI_args()

    try:
        data, fs = sf.read(cli_args.wavefile_name, dtype=np.float32)

        print(f"Framerate: {fs}")

        sd.play(data, fs)
        status = sd.wait()
    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
    if status:
        exit('Error during playback: ' + str(status))
