import numpy as np
from scipy.ndimage import gaussian_filter1d


def apply_attenuation(
    optical_power,
    attenuation_db_per_km,
    fiber_length_km
):
    """
    Apply optical fiber attenuation.
    """

    total_loss_db = (
        attenuation_db_per_km
        * fiber_length_km
    )

    transmission_factor = (
        10 ** (-total_loss_db / 10)
    )

    received_power = (
        optical_power
        * transmission_factor
    )

    return received_power, transmission_factor


def apply_dispersion(
    optical_power,
    dispersion_sigma
):
    """
    Apply simplified numerical dispersion
    using Gaussian filtering.
    """

    if dispersion_sigma == 0:
        return optical_power.copy()

    return gaussian_filter1d(
        optical_power,
        sigma=dispersion_sigma,
        mode="nearest"
    )