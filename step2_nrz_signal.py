import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Generate random binary data
# --------------------------------------------------

np.random.seed(42)

num_bits = 20

bits = np.random.randint(0, 2, num_bits)


# --------------------------------------------------
# 2. Communication system parameters
# --------------------------------------------------

bit_rate = 10e9       # 10 Gbps

bit_duration = 1 / bit_rate

samples_per_bit = 50

dt = bit_duration / samples_per_bit


# --------------------------------------------------
# 3. Convert bits into an NRZ waveform
# --------------------------------------------------

nrz_signal = np.repeat(bits, samples_per_bit)


# --------------------------------------------------
# 4. Create the time axis
# --------------------------------------------------

total_samples = len(nrz_signal)

time = np.arange(total_samples) * dt


# --------------------------------------------------
# 5. Display parameters
# --------------------------------------------------

print("Number of bits:", num_bits)
print("Bit rate:", bit_rate / 1e9, "Gbps")
print("Bit duration:", bit_duration * 1e12, "ps")
print("Samples per bit:", samples_per_bit)
print("Time step:", dt * 1e12, "ps")


# --------------------------------------------------
# 6. Plot the NRZ waveform
# --------------------------------------------------

plt.figure(figsize=(10, 4))

plt.plot(
    time * 1e9,
    nrz_signal
)

plt.title("10 Gbps NRZ Electrical Signal")
plt.xlabel("Time (ns)")
plt.ylabel("Voltage (V)")

plt.ylim(-0.2, 1.2)

plt.grid(True)

plt.tight_layout()

plt.show()