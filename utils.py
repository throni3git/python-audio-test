import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf


@dataclass
class ICLIArgs:
    wavefile_name: str


def write_soundfile(filename: str, data: np.ndarray, fs: int = 48000) -> None:
    fn_out_file = Path(filename)
    if not fn_out_file.parent.exists():
        fn_out_file.parent.mkdir()
    sf.write(fn_out_file.absolute(), data, fs, subtype="PCM_24")


def get_CLI_args() -> ICLIArgs:
    """ default CLI argument handling for all test cases """

    parser = argparse.ArgumentParser("play wavefile")
    parser.add_argument('wavefile_name', default="examples/click.wav", type=str, nargs='?', help='play this file')
    args = parser.parse_args()
    result = ICLIArgs(wavefile_name=args.wavefile_name)
    return result
