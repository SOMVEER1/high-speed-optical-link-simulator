import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# --------------------------------------------------
# 1. Generate random binary data
# --------------------------------------------------

np.random.seed(42)

num_bits = 20

bits = np.random.randint(
    0,
    2,
    num_bits
)


# --------------------------------------------------
# 2. Communication parameters
# --------------------------------------------------

bit_rate = 10e9

bit_duration = 1 / bit_rate

samples_per_bit = 50

dt = bit_duration / samples_per_bit


# --------------------------------------------------
# 3. Generate NRZ electrical waveform
# --------------------------------------------------

nrz_signal = np.repeat(
    bits,
    samples_per_bit
)


# --------------------------------------------------
# 4. Create time axis
# --------------------------------------------------

total_samples = len(nrz_signal)

time = np.arange(
    total_samples
) * dt


# --------------------------------------------------
# 5. Optical transmitter
# --------------------------------------------------

P_low = 0.1e-3

P_high = 1.0e-3

optical_power_tx = (
    P_low
    + (P_high - P_low)
    * nrz_signal
)


# --------------------------------------------------
# 6. Fiber attenuation
# --------------------------------------------------

attenuation_db_per_km = 0.2

fiber_length_km = 50

total_loss_db = (
    attenuation_db_per_km
    * fiber_length_km
)

transmission_factor = 10 ** (
    -total_loss_db / 10
)

optical_power_attenuated = (
    optical_power_tx
    * transmission_factor
)


# --------------------------------------------------
# 7. Simplified chromatic dispersion model
# --------------------------------------------------

# Controls pulse broadening
dispersion_sigma_samples = 12

optical_power_dispersed = (
    gaussian_filter1d(
        optical_power_attenuated,
        sigma=dispersion_sigma_samples,
        mode="nearest"
    )
)


# --------------------------------------------------
# 8. Display information
# --------------------------------------------------

print("Bit rate:",
      bit_rate / 1e9,
      "Gbps")

print("Fiber length:",
      fiber_length_km,
      "km")

print("Samples per bit:",
      samples_per_bit)

print("Dispersion sigma:",
      dispersion_sigma_samples,
      "samples")


# --------------------------------------------------
# 9. Plot first 10 bits
# --------------------------------------------------

plot_bits = 10

plot_samples = (
    plot_bits
    * samples_per_bit
)


plt.figure(figsize=(10, 5))

plt.plot(
    time[:plot_samples] * 1e9,
    optical_power_attenuated[:plot_samples] * 1e3,
    label="Without Dispersion"
)

plt.plot(
    time[:plot_samples] * 1e9,
    optical_power_dispersed[:plot_samples] * 1e3,
    label="With Simplified Dispersion"
)

plt.title(
    "Effect of Chromatic Dispersion on Optical Signal"
)

plt.xlabel("Time (ns)")

plt.ylabel("Optical Power (mW)")

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()