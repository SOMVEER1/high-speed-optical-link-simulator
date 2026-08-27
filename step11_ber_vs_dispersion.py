import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# --------------------------------------------------
# 1. Simulation parameters
# --------------------------------------------------

np.random.seed(42)

num_bits = 100000

bit_rate = 10e9
bit_duration = 1 / bit_rate

samples_per_bit = 50

# Optical transmitter
P_low = 0.1e-3
P_high = 1.0e-3

# Fiber
attenuation_db_per_km = 0.2
fiber_length_km = 50

# Photodetector
responsivity = 0.8  # A/W

# Receiver noise
noise_std = 0.03e-3  # A


# --------------------------------------------------
# 2. Generate random bits
# --------------------------------------------------

bits = np.random.randint(
    0,
    2,
    num_bits
)


# --------------------------------------------------
# 3. Generate NRZ waveform
# --------------------------------------------------

nrz_signal = np.repeat(
    bits,
    samples_per_bit
)


# --------------------------------------------------
# 4. Optical transmitter
# --------------------------------------------------

optical_power_tx = (
    P_low
    + (P_high - P_low) * nrz_signal
)


# --------------------------------------------------
# 5. Fiber attenuation
# --------------------------------------------------

total_loss_db = (
    attenuation_db_per_km
    * fiber_length_km
)

transmission_factor = 10 ** (
    -total_loss_db / 10
)

optical_power_rx = (
    optical_power_tx
    * transmission_factor
)


# --------------------------------------------------
# 6. Calculate ideal receiver levels
# --------------------------------------------------

I_low = (
    responsivity
    * P_low
    * transmission_factor
)

I_high = (
    responsivity
    * P_high
    * transmission_factor
)

threshold = (
    I_low + I_high
) / 2


# --------------------------------------------------
# 7. Dispersion strengths to test
# --------------------------------------------------

dispersion_values = [
    0,
    2,
    4,
    6,
    8,
    10,
    12,
    16,
    20
]


# --------------------------------------------------
# 8. Sampling positions
# --------------------------------------------------

sample_indices = (
    np.arange(num_bits)
    * samples_per_bit
    + samples_per_bit // 2
)


# --------------------------------------------------
# 9. Store BER results
# --------------------------------------------------

ber_values = []


# --------------------------------------------------
# 10. Run simulation
# --------------------------------------------------

for sigma in dispersion_values:

    # ----------------------------------------------
    # Apply simplified dispersion
    # ----------------------------------------------

    if sigma == 0:

        dispersed_power = optical_power_rx.copy()

    else:

        dispersed_power = gaussian_filter1d(
            optical_power_rx,
            sigma=sigma,
            mode="nearest"
        )


    # ----------------------------------------------
    # Photodetector
    # ----------------------------------------------

    photocurrent = (
        responsivity
        * dispersed_power
    )


    # ----------------------------------------------
    # Sample at center of each bit
    # ----------------------------------------------

    received_samples = (
        photocurrent[sample_indices]
    )


    # ----------------------------------------------
    # Add Gaussian noise
    # ----------------------------------------------

    noise = np.random.normal(
        loc=0,
        scale=noise_std,
        size=num_bits
    )

    noisy_samples = (
        received_samples
        + noise
    )


    # ----------------------------------------------
    # Receiver decision
    # ----------------------------------------------

    received_bits = (
        noisy_samples > threshold
    ).astype(int)


    # ----------------------------------------------
    # Calculate BER
    # ----------------------------------------------

    errors = np.sum(
        bits != received_bits
    )

    ber = errors / num_bits

    ber_values.append(ber)


    print(
        f"Dispersion sigma: {sigma:2d} samples | "
        f"Errors: {errors:5d} | "
        f"BER: {ber:.6e}"
    )


# --------------------------------------------------
# 11. Convert to NumPy array
# --------------------------------------------------

ber_values = np.array(
    ber_values
)


# --------------------------------------------------
# 12. Plot BER vs dispersion
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.semilogy(
    dispersion_values,
    ber_values,
    marker="o"
)

plt.title(
    "BER vs Simplified Dispersion Strength"
)

plt.xlabel(
    "Gaussian Dispersion Sigma (samples)"
)

plt.ylabel(
    "Bit Error Rate (BER)"
)

plt.grid(True, which="both")

plt.tight_layout()

plt.show()