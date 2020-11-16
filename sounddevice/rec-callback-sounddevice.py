import argparse
import sys
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf


if __name__ == "__main__":

    parser = argparse.ArgumentParser("play wavefile")
    # parser.add_argument('wavefile_name', default="examples/click.wav",
    #                     type=str, nargs='?', help='use this file to play')
    args = parser.parse_args()

    try:

        fs = 48000
        # data, fs = sf.read(args.wavefile_name, dtype=np.float32)

        # print(f"Framerate: {fs}")
        duration = 3 * fs
        data = np.zeros((duration, 2), dtype=np.float32)

        pt_data = 0
        # sd.play(data, fs)
        # status = sd.wait()

        def callback_input(indata, frames, time, status):
            import time
            global data
            global pt_data
            # print(time.time_ns()/1e6)
            if status:
                print(status)

            out_length = frames
            if pt_data + out_length > data.shape[0]:
                out_length -= pt_data + out_length - data.shape[0]
            # print(out_length)

            # print(data.shape)
            # print(indata.shape)

            if out_length > 0:
                snippet = indata[:out_length, :]

                level = np.sqrt(np.mean(snippet ** 2))
                if not np.isnan(level) :
                    anzeige = '#' * int(level*80)
                    print(anzeige)

                data[pt_data:pt_data+out_length, :] = snippet
                pt_data += out_length

        blocksize = 1024
        stream = sd.InputStream(
            samplerate=fs,
            blocksize=blocksize,
            channels=2,
            dtype='float32',
            callback=callback_input)
        with stream:
            timeout = blocksize / fs
            while pt_data < data.shape[0]:
                sd.sleep(int(timeout*1000))
        
        fn_out_file = Path("tmp/rec-callback-sounddevice.wav")
        if not fn_out_file.parent.exists():
            fn_out_file.parent.mkdir()
        sf.write(fn_out_file.absolute(), data, fs)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
    # if status:
    #     parser.exit('Error during playback: ' + str(status))
