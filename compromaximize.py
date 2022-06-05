import argparse
from pathlib import Path

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


if __name__ == '__main__':
    DBG = False

    cli_args = utils.get_CLI_args()

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

        maximized = compromaximize(data, fs, 0.1, limit_gain=100, dbg=DBG)

        fn_out = Path("tmp") / f"{fn_in.stem}_compromaximized.wav"
        utils.write_soundfile(fn_out, maximized.T, fs)

    if DBG:
        plt.show()
