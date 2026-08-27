import numpy as np


def generate_bits(num_bits, seed=None):
    """
    Generate random binary data.
    """

    if seed is not None:
        np.random.seed(seed)

    return np.random.randint(
        0,
        2,
        num_bits
    )


def create_nrz(bits, samples_per_bit):
    """
    Convert binary data into an NRZ waveform.
    """

    return np.repeat(
        bits,
        samples_per_bit
    )


def optical_transmitter(
    nrz_signal,
    P_low,
    P_high
):
    """
    Convert electrical NRZ signal into
    optical power levels.
    """

    optical_power = (
        P_low
        + (P_high - P_low)
        * nrz_signal
    )

    return optical_power