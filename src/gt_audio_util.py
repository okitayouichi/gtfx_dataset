"""
Utility classes and functions for processing guitar audio and effect.
"""

import os
import soundfile as sf
import numpy as np


class GuitarInfo:
    """
    Information about guitar play.

    Attributes:
        guitar(str): Guitar name.
        string(int): String number. From low to high pitch. 1-based.
        fret(int): Fret number. From low to high pitch. 0-based
        fx(FxInfo): Guitar effect information.
    """

    def __init__(self, guitar, string, fret):
        self.guitar = guitar
        self.string = string
        self.fret = fret

    def add_fx(self, type, params=None):
        self.fx = FxInfo(type, params)


class FxInfo:
    """
    Information about guitar audio effect.

    Attributes:
        type(str): Effect type.
        params(dict[str, float]): Effect parameter names and their values.
    """

    def __init__(self, type, params=None):
        self.type = type
        self.params = params or {}


def load_audio(path):
    """
    Load an audio file and get a signal.

    Args:
        path(pathlib.Path): Path to the audio file.

    Returns:
        signal(numpy.ndarray): Audio signal.
        sample_rate(int): Sampling rate.
    """
    signal, sample_rate = sf.read(path)
    return signal, sample_rate


def save_audio(path, signal, sample_rate):
    """
    Exporting an audio file from a signal.

    Args:
        path(pathlib.Path): Path to the audio file.
        signal(numpy.ndarray): Audio signal.
        sample_rate(int): Sampling rate.
    """
    os.makedirs(path.parent, exist_ok=True)
    sf.write(path, signal, sample_rate)


def norm_loudness(signal, rms_target=0.1, eps=1.0e-8):
    """
    Normalize the loudness of an audio signal by the root-mean-square.

    Args:
        signal(numpy.ndarray[numpy.float64]): Audio signal whose values range in [-1.0, 1.0).
        rms_target(float): Target value of root-mean-square.
        eps(float): Small value to avoid division by zero.

    Returns:
        signal(numpy.ndarray[numpy.float64]): Audio signal which loudness is normalized.
    """
    rms = np.sqrt(np.mean(signal**2))
    rms = max(rms, eps)
    signal = signal / rms * rms_target
    return signal
