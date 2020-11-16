import argparse
import sys
import time

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

        pt_data = 0
        # sd.play(data, fs)
        # status = sd.wait()

        def callback(indata, outdata, frames, time, status):
            import time
            print(time.time_ns()/1e6)
            if status:
                print(status)
            outdata[:] = indata

        def callback_output(outdata, frames, time, status):
            import time
            global data
            global pt_data
            print(time.time_ns()/1e6)
            if status:
                print(status)

            out_length = frames
            if pt_data + out_length > data.shape[0]:
                out_length -= pt_data + out_length - data.shape[0]
            print(out_length)

            outdata[:out_length, 0] = data[pt_data:pt_data+out_length]
            outdata[:out_length, 1] = data[pt_data:pt_data+out_length]
            pt_data += out_length

        blocksize = 1024//4
        stream = sd.OutputStream(
            samplerate=fs,
            blocksize=blocksize,
            channels=2,
            dtype='float32',
            callback=callback_output)
        with stream:
            timeout = blocksize / fs
            while pt_data < data.shape[0]:
                sd.sleep(int(timeout*1000))

    except KeyboardInterrupt:
        parser.exit('\nInterrupted by user')
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))
    # if status:
    #     parser.exit('Error during playback: ' + str(status))
