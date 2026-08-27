import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Generate random binary data
# --------------------------------------------------

np.random.seed(42)

num_bits = 20
bits = np.random.randint(0, 2, num_bits)


# --------------------------------------------------
# 2. Communication parameters
# --------------------------------------------------

bit_rate = 10e9
bit_duration = 1 / bit_rate

samples_per_bit = 50
dt = bit_duration / samples_per_bit


# --------------------------------------------------
# 3. Generate NRZ electrical signal
# --------------------------------------------------

nrz_signal = np.repeat(bits, samples_per_bit)


# --------------------------------------------------
# 4. Create time axis
# --------------------------------------------------

total_samples = len(nrz_signal)
time = np.arange(total_samples) * dt


# --------------------------------------------------
# 5. Optical transmitter
# --------------------------------------------------

P_low = 0.1e-3
P_high = 1.0e-3

optical_power_tx = (
    P_low
    + (P_high - P_low) * nrz_signal
)


# --------------------------------------------------
# 6. Optical fiber attenuation
# --------------------------------------------------

attenuation_db_per_km = 0.2
fiber_length_km = 10

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
# 7. Photodetector model
# --------------------------------------------------

responsivity = 0.8  # A/W

photocurrent = (
    responsivity
    * optical_power_rx
)


# --------------------------------------------------
# 8. Add Gaussian noise
# --------------------------------------------------

noise_std = 0.05e-3  # 0.05 mA

noise = np.random.normal(
    loc=0,
    scale=noise_std,
    size=len(photocurrent)
)

noisy_photocurrent = (
    photocurrent + noise
)


# --------------------------------------------------
# 9. Display information
# --------------------------------------------------

print("Noise standard deviation:",
      noise_std * 1e3, "mA")

print("Maximum clean current:",
      np.max(photocurrent) * 1e3, "mA")

print("Maximum noisy current:",
      np.max(noisy_photocurrent) * 1e3, "mA")


# --------------------------------------------------
# 10. Plot clean and noisy signals
# --------------------------------------------------

plt.figure(figsize=(10, 4))

plt.plot(
    time * 1e9,
    photocurrent * 1e3,
    label="Clean Signal"
)

plt.plot(
    time * 1e9,
    noisy_photocurrent * 1e3,
    alpha=0.7,
    label="Noisy Signal"
)

plt.title("Photodetector Output with Gaussian Noise")
plt.xlabel("Time (ns)")
plt.ylabel("Photocurrent (mA)")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()