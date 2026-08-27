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
# 6. Optical fiber parameters
# --------------------------------------------------

attenuation_db_per_km = 0.2
fiber_length_km = 10


# --------------------------------------------------
# 7. Calculate total fiber loss
# --------------------------------------------------

total_loss_db = (
    attenuation_db_per_km
    * fiber_length_km
)


# --------------------------------------------------
# 8. Calculate transmission factor
# --------------------------------------------------

transmission_factor = 10 ** (
    -total_loss_db / 10
)


# --------------------------------------------------
# 9. Apply fiber attenuation
# --------------------------------------------------

optical_power_rx = (
    optical_power_tx
    * transmission_factor
)


# --------------------------------------------------
# 10. Display results
# --------------------------------------------------

print("Fiber length:", fiber_length_km, "km")
print(
    "Attenuation:",
    attenuation_db_per_km,
    "dB/km"
)

print("Total fiber loss:", total_loss_db, "dB")

print(
    "Transmission factor:",
    round(transmission_factor, 4)
)

print(
    "Maximum transmitted power:",
    P_high * 1e3,
    "mW"
)

print(
    "Maximum received power:",
    np.max(optical_power_rx) * 1e3,
    "mW"
)


# --------------------------------------------------
# 11. Plot transmitted optical signal
# --------------------------------------------------

plt.figure(figsize=(10, 4))

plt.plot(
    time * 1e9,
    optical_power_tx * 1e3,
    label="Transmitted Optical Power"
)

plt.title("Optical Signal Before Fiber")
plt.xlabel("Time (ns)")
plt.ylabel("Optical Power (mW)")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


# --------------------------------------------------
# 12. Plot received optical signal
# --------------------------------------------------

plt.figure(figsize=(10, 4))

plt.plot(
    time * 1e9,
    optical_power_rx * 1e3,
    label="Received Optical Power"
)

plt.title("Optical Signal After 10 km Fiber")
plt.xlabel("Time (ns)")
plt.ylabel("Optical Power (mW)")

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()