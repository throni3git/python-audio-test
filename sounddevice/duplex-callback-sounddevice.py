import sys

import numpy as np
import sounddevice as sd
import soundfile as sf

import utils


if __name__ == "__main__":

    cli_args = utils.get_CLI_args()

    try:

        sweep_data, fs = sf.read(cli_args.wavefile_name, dtype=np.float32)
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

        # sd.default.device = "JACK"
        blocksize = 128
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

        utils.write_soundfile("tmp/duplex-callback-sounddevice.wav", record_data, fs)

    except KeyboardInterrupt:
        exit('\nInterrupted by user')
    except Exception as e:
        exit(type(e).__name__ + ': ' + str(e))
