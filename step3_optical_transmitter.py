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
# 5. Optical transmitter parameters
# --------------------------------------------------

P_low = 0.1e-3     # 0.1 mW in watts
P_high = 1.0e-3    # 1.0 mW in watts


# --------------------------------------------------
# 6. Electrical-to-optical conversion
# --------------------------------------------------

optical_power = P_low + (P_high - P_low) * nrz_signal


# --------------------------------------------------
# 7. Display information
# --------------------------------------------------

print("Bit rate:", bit_rate / 1e9, "Gbps")
print("Low optical power:", P_low * 1e3, "mW")
print("High optical power:", P_high * 1e3, "mW")


# --------------------------------------------------
# 8. Plot electrical signal
# --------------------------------------------------

plt.figure(figsize=(10, 4))

plt.plot(time * 1e9, nrz_signal)

plt.title("Electrical NRZ Signal")
plt.xlabel("Time (ns)")
plt.ylabel("Normalized Voltage")

plt.ylim(-0.2, 1.2)
plt.grid(True)

plt.tight_layout()
plt.show()


# --------------------------------------------------
# 9. Plot optical power
# --------------------------------------------------

plt.figure(figsize=(10, 4))

plt.plot(time * 1e9, optical_power * 1e3)

plt.title("Optical Transmitter Output")
plt.xlabel("Time (ns)")
plt.ylabel("Optical Power (mW)")

plt.grid(True)

plt.tight_layout()
plt.show()