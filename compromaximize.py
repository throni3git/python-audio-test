from pathlib import Path
import time

import numpy as np
import scipy.signal

import utils


class Compromaximizer:
    """ dynamically compresses music blockwise up to a certain limit
    """

    def __init__(self, limit_gain: float = 10.0):
        self.blocksize: int = None
        self.limit_gain: float = limit_gain
        self.window: np.ndarray = None

    def _compromaximize_one_block(self, in_block: np.ndarray) -> np.ndarray:
        """processes one block

        Parameters
        ----------
        in_data : np.ndarray
            raw block of shape (channels, samples)

        Returns
        -------
        np.ndarray
            processed block
        """

        # window before processing
        windowed_data = in_block * self.window[None, :]

        # get gain factor
        abs_block = np.abs(windowed_data)
        max_value = float(np.max(abs_block))
        if max_value == 0.0:
            max_value = 1e-9
        max_gain = 1.0 / max_value
        gain = min(max_gain, self.limit_gain)

        # apply on result
        result = windowed_data * gain
        return result

    def process(self, in_data: np.ndarray, fs: int, window_duration: float = 0.1) -> np.ndarray:
        """takes a whole sound array and processes it blockwise

        Parameters
        ----------
        in_data : np.ndarray
            incoming audio of shape (channels, samples)

        Returns
        -------
        np.ndarray
            processed audio
        """

        if in_data.ndim > 2:
            raise ValueError("too much dimensions as input signal")
        if in_data.ndim == 1:
            in_data = np.atleast_2d(in_data)

        blocksize = int(fs * window_duration * 2) // 2
        overlap = 4
        hopsize = blocksize // overlap
        self.window = scipy.signal.windows.hann(blocksize).astype('float32')

        # padding calculations
        channels = in_data.shape[0]
        original_length = in_data.shape[1]
        amount_blocks = int(np.ceil(original_length / hopsize))
        padded_length = int(amount_blocks * hopsize)
        result = np.zeros((channels, padded_length))

        for idx in range(amount_blocks-overlap+1):
            start = idx * hopsize
            if idx == amount_blocks - overlap:
                current = np.zeros((channels, blocksize))
                remaining_samples = original_length - start
                end = start + remaining_samples
                current[:, :remaining_samples] = in_data[:, start:end]
            else:
                current = in_data[:, start:start+blocksize]

            processed = self._compromaximize_one_block(current)
            result[:, start:start+blocksize] += processed

        # shorten and return
        result = result[:, :original_length]
        return result / overlap


def main_example():
    """example for using Compromaximizer
    """

    fn_in = Path(__file__).parent / "examples/sprache.wav"
    # fn_in = Path("D:/Bands/Entleerung Schmidt/Entleerung_2022-02-27/220227_0168.wav")

    data, fs = utils.load_soundfile(fn_in)

    comp = Compromaximizer(20)
    start = time.time()
    maximized = comp.process(data, fs, 1.0)
    end = time.time()
    print(f"it took {end-start}")

    fn_out = Path("tmp") / f"{fn_in.stem}_compromaximizedNEU.wav"
    utils.write_soundfile(fn_out, maximized.T, fs)


def main_multiple():
    """process files in a loop
    """

    comp = Compromaximizer()

    fns = [
        "D:/Bands/Entleerung Schmidt/Entleerung_2022-02-27/220227_0168.wav",
        "D:/Bands/Entleerung Schmidt/Entleerung_2022-02-27/220227_0169A.wav",
        "D:/Bands/Entleerung Schmidt/Entleerung_2022-02-27/220227_0169.wav"
    ]

    for fn_in in fns:
        fn_in = Path(fn_in)
        print(f"processing file {fn_in}")
        data, fs = utils.load_soundfile(fn_in)

        data = data - np.mean(data, axis=1)[:, None]

        maximized = comp.process(data, fs, 0.1)

        fn_out = Path("tmp") / f"{fn_in.stem}_compromaximized.wav"
        utils.write_soundfile(fn_out, maximized.T, fs)


if __name__ == '__main__':
    main_example()
    # main_multiple()
