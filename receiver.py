import numpy as np


def photodetector(
    optical_power,
    responsivity
):
    """
    Convert optical power into photocurrent.
    """

    return (
        responsivity
        * optical_power
    )


def add_noise(
    signal,
    noise_std
):
    """
    Add Gaussian noise.
    """

    noise = np.random.normal(
        loc=0,
        scale=noise_std,
        size=len(signal)
    )

    return signal + noise


def sample_signal(
    signal,
    num_bits,
    samples_per_bit
):
    """
    Sample at the center of every bit.
    """

    sample_indices = (
        np.arange(num_bits)
        * samples_per_bit
        + samples_per_bit // 2
    )

    return signal[sample_indices]


def make_decision(
    received_samples,
    threshold
):
    """
    Convert received signal samples
    into binary decisions.
    """

    return (
        received_samples > threshold
    ).astype(int)