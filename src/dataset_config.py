"""
Data and functions for guitar effects dataset configuration.
"""

import gt_audio_util as util
import pedalboard as pb
import numpy as np
from pathlib import Path
import os
import json
from dotenv import load_dotenv

# constant
num_grid = 1  # number of iterations of effect parameter change

# path
load_dotenv()
project_path = Path(os.getenv("PROJECT_PATH"))  # path to the audio effect estimation project
dataset_path = project_path / "gtfx_dataset"  # path to the directory of the dataset you are about to create
dry_signals_path = project_path / "gt_dataset"  # path to the directory containing audio of guitar dry signals

# guitar class
guitars = {
    "sc": "data/sc/audio",
    "tc": "data/tc/audio",
    "lp": "data/lp/audio",
}  # guitars and relative paths from dry_signals_path to their audio file
strings = range(1, 7)  # string numbers, from low to high pitch, 1-based
frets = range(20)  # fret numbers, from low to high pitch, 0-based

# effect class
fxs = {
    # "chorus": {"plugin": pb.Chorus, "params": {"rate_hz": np.linspace(0.1, 5.0, num_grid), "depth": np.linspace(0.05, 0.4, num_grid)}},
    "distortion": {"plugin": pb.Distortion, "params": {"drive_db": np.linspace(10.0, 50.0, num_grid)}},
    # "phaser": {"plugin": pb.Phaser, "params": {"rate_hz": np.linspace(0.1, 5.0, num_grid), "depth": np.linspace(0.05, 0.4, num_grid)}},
    "reverb": {"plugin": pb.Reverb, "params": {"room_size": np.linspace(0.1, 1.0, num_grid)}},
}  # guitar effects, plugins and their variable parameters
# the dataset for "fx_estimate" excludes "chorus" and "phaser"


def make_dataset(guitar_info, data_num):
    """
    Generate a dataset of guitar wet signal.

    Args:
        guitar_info(gt_audio_util.GuitarInfo): Information about the guitar play to be processed.
        data_num(int): The first serial number of the data to be created.

    Returns:
        data_num(int): The last serial number of the data created.
    """
    dry_signal_path = get_dry_signal_path(guitar_info)
    dry_signal, sample_rate = util.load_audio(dry_signal_path)
    dry_signal = util.norm_loudness(dry_signal)
    param_names = list(fxs[guitar_info.fx.type]["params"].keys())
    param_vals = [fxs[guitar_info.fx.type]["params"][param_name] for param_name in param_names]  # 2d list containing variable parameter values
    data_num = fx_grid(guitar_info, dry_signal, sample_rate, data_num, param_names, param_vals)
    return data_num


def fx_grid(guitar_info, dry_signal, sample_rate, data_num, param_names, param_vals, current_params=None, param_num=0):
    """
    Apply an effect its parameters vary to a dry signal and save its label and audio.

    Args:
        guitar_info(GuitarInfo): Information about the guitar play to be processed.
        dry_signal(numpy.ndarray): Dry signal to be processed.
        sample_rate(int): Sampling rate of dry signal.
        data_num(int): Serial number of the data to be generated.
        param_names(list[str]): Variable parameter names.
        param_vals(list[float]): 2d list containing variable parameter values.
        current_params(dict[str, float]): Current applied effect parameter names and their values.
        param_num(int): Varying parameter number. Depth of recursive calls of this function.

    Returns:
        data_num(int): Serial number of the data just generated.
    """
    if current_params is None:
        # first call
        current_params = {}
    if param_num == len(param_names):
        plugin = fxs[guitar_info.fx.type]["plugin"]
        board = pb.Pedalboard([plugin(**current_params)])
        wet_signal = board(dry_signal, sample_rate)
        guitar_info.fx.params = current_params
        label_path = get_label_path(guitar_info, data_num)
        wet_signal_path = get_wet_signal_path(guitar_info, data_num)
        save_label(label_path, guitar_info)
        util.save_audio(wet_signal_path, wet_signal, sample_rate)
        data_num += 1
        return data_num
    else:
        param_name = param_names[param_num]
        for val in param_vals[param_num]:
            current_params[param_name] = val
            data_num = fx_grid(guitar_info, dry_signal, sample_rate, data_num, param_names, param_vals, current_params, param_num + 1)
        return data_num


def save_label(label_path, guitar_info):
    """
    Save label for wet signal.

    Args:
        label_path(pathlib.Path): Path to the label.
        guitar_info(gt_audio_util.GuitarInfo): Information about guitar play to be labeled.
    """
    label = {"guitar": guitar_info.guitar, "string": guitar_info.string, "fret": guitar_info.fret, "fx": {"type": guitar_info.fx.type, "params": guitar_info.fx.params}}
    os.makedirs(label_path.parent, exist_ok=True)
    with open(label_path, "w") as f:
        json.dump(label, f, indent=2)
        f.write("\n")


def get_dry_signal_path(guitar_info):
    """
    Get path to the dry signal.

    Args:
        guitar_info(gt_audio_util.GuitarInfo): Information about guitar play.

    Returns:
        path(pathlib.Path): Path to the dry signal audio file.
    """
    num_data_guitar = len(strings) * len(frets)
    if guitar_info.guitar == "sc":
        data_num = 0 * num_data_guitar
    elif guitar_info.guitar == "tc":
        data_num = 1 * num_data_guitar
    elif guitar_info.guitar == "lp":
        data_num = 2 * num_data_guitar
    data_num += (guitar_info.string - 1) * len(frets) + guitar_info.fret
    path = dry_signals_path / guitars[guitar_info.guitar] / ("gt" + str(data_num).zfill(8) + ".flac")
    return path


def get_wet_signal_path(guitar_info, data_num):
    """
    Generate path to the wet signal.

    Args:
        guitar_info(gt_audio_util.GuitarInfo): Information about guitar play.
        data_num(int): Data serial number.

    Returns:
        path(pathlib.Path): Path to the wet signal audio file.
    """
    path = dataset_path / "data" / guitar_info.guitar / guitar_info.fx.type / "audio" / ("gtfx" + str(data_num).zfill(8) + ".flac")
    return path


def get_label_path(guitar_info, data_num):
    """
    Generate path to the wet signal.

    Args:
        guitar_info(gt_audio_util.GuitarInfo): Information about guitar play.
        data_num(int): Data serial number.

    Returns:
        path(pathlib.Path): Path to the label for wet signal.
    """
    path = dataset_path / "data" / guitar_info.guitar / guitar_info.fx.type / "label" / ("gtfx" + str(data_num).zfill(8) + ".json")
    return path
