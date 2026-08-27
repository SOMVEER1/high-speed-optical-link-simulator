import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Generate random binary data
# --------------------------------------------------

np.random.seed(42)

num_bits = 1000
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
# 7. Photodetector
# --------------------------------------------------

responsivity = 0.8

photocurrent = (
    responsivity
    * optical_power_rx
)


# --------------------------------------------------
# 8. Add Gaussian noise
# --------------------------------------------------

noise_std = 0.05e-3

noise = np.random.normal(
    loc=0,
    scale=noise_std,
    size=len(photocurrent)
)

noisy_photocurrent = (
    photocurrent + noise
)


# --------------------------------------------------
# 9. Sample at the center of each bit
# --------------------------------------------------

sample_indices = (
    np.arange(num_bits)
    * samples_per_bit
    + samples_per_bit // 2
)

received_samples = (
    noisy_photocurrent[sample_indices]
)


# --------------------------------------------------
# 10. Calculate decision threshold
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
# 11. Make receiver decision
# --------------------------------------------------

received_bits = (
    received_samples > threshold
).astype(int)


# --------------------------------------------------
# 12. Calculate errors and BER
# --------------------------------------------------

errors = np.sum(
    bits != received_bits
)

ber = errors / num_bits


# --------------------------------------------------
# 13. Display results
# --------------------------------------------------

print("Number of transmitted bits:", num_bits)

print("Fiber length:",
      fiber_length_km, "km")

print("Noise standard deviation:",
      noise_std * 1e3, "mA")

print("Decision threshold:",
      threshold * 1e3, "mA")

print("Number of bit errors:",
      errors)

print("Bit Error Rate (BER):",
      ber)


# --------------------------------------------------
# 14. Show first 20 transmitted and received bits
# --------------------------------------------------

print("\nFirst 20 bits:")

print("Transmitted:")
print(bits[:20])

print("Received:")
print(received_bits[:20])


# --------------------------------------------------
# 15. Plot first 10 bits
# --------------------------------------------------

plot_bits = 10

plot_samples = (
    plot_bits
    * samples_per_bit
)

plt.figure(figsize=(10, 4))

plt.plot(
    time[:plot_samples] * 1e9,
    noisy_photocurrent[:plot_samples] * 1e3,
    label="Noisy Photocurrent"
)

plt.axhline(
    threshold * 1e3,
    linestyle="--",
    label="Decision Threshold"
)

plt.title("Receiver Signal and Decision Threshold")
plt.xlabel("Time (ns)")
plt.ylabel("Photocurrent (mA)")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()