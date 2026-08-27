import numpy as np


def calculate_ber(
    transmitted_bits,
    received_bits
):
    """
    Calculate number of errors
    and Bit Error Rate.
    """

    errors = np.sum(
        transmitted_bits
        != received_bits
    )

    ber = (
        errors
        / len(transmitted_bits)
    )

    return errors, ber