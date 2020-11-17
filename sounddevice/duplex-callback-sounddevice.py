import argparse
import sys
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf


if __name__ == "__main__":

    parser = argparse.ArgumentParser("play wavefile")
    parser.add_argument('wavefile_name', default="examples/sweep_noise.wav",
                        type=str, nargs='?', help='use this file to play')
    args = parser.parse_args()

    try:

        sweep_data, fs = sf.read(args.wavefile_name, dtype=np.float32)
        sweep_data = np.atleast_2d(sweep_data).T

        print(f"Framerate: {fs}")

        duration = sweep_data.shape[0]
        record_data = np.zeros((duration, 2), dtype=np.float32)

        pt_data = 0
        # sd.play(data, fs)
        # status = sd.wait()

        def callback_duplex(indata, outdata, frames, time, status):
            import time
            # print(time.time_ns()/1e6)

            global sweep_data
            global pt_data

            if 'debugpy' in sys.modules:
                import debugpy
                debugpy.debug_this_thread()

            if status:
                print(status)

            out_length = frames
            if pt_data + out_length > record_data.shape[0]:
                out_length -= pt_data + out_length - record_data.shape[0]
            # print(out_length)

            # print(data.shape)
            # print(indata.shape)

            if out_length > 0:
                snippet = sweep_data[pt_data:pt_data+out_length, :]

                # level = np.sqrt(np.mean(snippet ** 2))
                # if not np.isnan(level):
                #     anzeige = '#' * int(level*80)
                #     print(anzeige)

                outdata[:out_length, :] = snippet
                pt_data += out_length

                if pt_data+out_length < record_data.shape[0]:
                    record_data[pt_data:pt_data+out_length, :] = indata[:out_length, :]

        blocksize = 32
        stream = sd.Stream(
            samplerate=fs,
            blocksize=blocksize,
            channels=2,
            dtype='float32',
            latency="low",
            callback=callback_duplex)

        with stream:
            timeout = blocksize / fs
            while pt_data < sweep_data.shape[0]:
                sd.sleep(int(timeout*1000))

        fn_out_file = Path("tmp/duplex-callback-sounddevice.wav")
        if not fn_out_file.parent.exists():
            fn_out_file.parent.mkdir()
        sf.write(fn_out_file.absolute(), record_data, fs)

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
    # if status:
    #     parser.exit('Error during playback: ' + str(status))
