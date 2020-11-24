import numpy as np
import sounddevice as sd

import utils


if __name__ == "__main__":

    cli_args = utils.get_CLI_args()

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
                if not np.isnan(level):
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

        utils.write_soundfile("tmp/rec-callback-sounddevice.wav", data, fs)

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
