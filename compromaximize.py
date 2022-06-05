import argparse
from pathlib import Path
import time

import numpy as np
import scipy.signal
import matplotlib.pyplot as plt

import utils


def compromaximize(data: np.ndarray, fs: int,
                   window_duration: float,
                   limit_gain: float = 10.0,
                   dbg: bool = False) -> np.ndarray:
    """Compresses audio signal piece by piece up to a factor of `limit_gain`.

    Parameters
    ----------
    data : np.ndarray
        input signal of shape (channels, samples)
    fs : int
        samplerate
    window_duration : float
        length of window for normalization
    limit_gain : float, optional
        maximum amount of gain for a block, by default `10.0`
    dbg : bool, optional
        debug flag, by default `False`

    Returns
    -------
    np.ndarray
        louder and compressed signal

    Raises
    ------
    ValueError
        input data must be of shape (channels, samples)
    """

    if data.ndim == 1:
        data = np.atleast_2d(data)
    if data.ndim > 2:
        raise ValueError("two many dimensions in input data")

    odd_length = data.shape[-1] % 2
    if odd_length == 1:
        data = np.pad(data, ((0, 0), (0, 1)))

    window_width = int(fs * window_duration/2)*2
    hop_size = window_width//2
    sample_idx = np.arange(window_width)

    if data.shape[-1] // hop_size % 2 == 0:
        data = np.pad(data, ((0, 0), (0, hop_size)))
        odd_length += hop_size
    block_idx = np.arange(data.shape[-1] // hop_size)

    if dbg:
        print(odd_length)

    matrix = block_idx[:, None]*hop_size + sample_idx[None, :]
    amount_samples = int(data.shape[-1] // window_width+1) * window_width

    # print(matrix)
    additional_samples = (amount_samples-data.shape[-1]) // 2
    data = np.pad(data, ((0, 0), (additional_samples, additional_samples)))
    matrix[matrix > data.shape[1]-1] = data.shape[1]-1
    blocks = data[:, matrix]

    window = scipy.signal.windows.hann(window_width).astype('float32')
    windowed = blocks * window[None, None, :]

    abs_blocks = np.abs(blocks)
    max_values = np.max(abs_blocks, axis=(0, 2))
    max_values[max_values < 1/limit_gain] = 1/limit_gain
    gains = 1 / max_values
    maximized = windowed * gains[None, :, None]
    del windowed

    odd_blocks = maximized[:, ::2, :]
    even_blocks = maximized[:, 1::2, :]
    del maximized
    recombined1 = np.reshape(odd_blocks, (data.shape[0], amount_samples))
    recombined2 = np.reshape(even_blocks, (data.shape[0], amount_samples-window_width))
    # plt.plot(recombined1.T)
    # plt.plot(recombined2.T)
    recombined = recombined1[:, hop_size:-hop_size] + recombined2

    if odd_length == 1:
        recombined = recombined[:, :-1]

    if dbg:
        # plt.plot(recombined.T)
        plt.plot(gains)

    return recombined


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
    DBG = False

    cli_args = utils.get_CLI_args()

    comp = Compromaximizer()

    # compromaximize(np.random.randn(2, 20), 1, 4)

    fns = [
        "D:/Bands/Entleerung Schmidt/Entleerung_2022-02-27/220227_0168.wav",
        "D:/Bands/Entleerung Schmidt/Entleerung_2022-02-27/220227_0169A.wav",
        "D:/Bands/Entleerung Schmidt/Entleerung_2022-02-27/220227_0169.wav"
    ]

    fn_in = cli_args.wavefile_name
    # fn_in = "examples/click.wav"
    # fn_in = "examples/sweep.wav"
    fn_in = "D:/Bands/Entleerung Schmidt/Entleerung_2022-03-18/220320_0183.wav"
    for fn_in in fns:
        fn_in = Path(fn_in)
        print(f"processing file {fn_in}")
        data, fs = utils.load_soundfile(fn_in)

        data = data - np.mean(data, axis=1)[:, None]

        # maximized = compromaximize(data, fs, 0.1, limit_gain=100, dbg=DBG)
        maximized = comp.process(data, fs, 0.1)

        fn_out = Path("tmp") / f"{fn_in.stem}_compromaximized.wav"
        utils.write_soundfile(fn_out, maximized.T, fs)

    if DBG:
        plt.show()


if __name__ == '__main__':
    main_example()
    # main_multiple()
