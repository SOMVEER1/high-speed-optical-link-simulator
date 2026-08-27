import numpy as np
import matplotlib.pyplot as plt

from modules.transmitter import (
    generate_bits,
    create_nrz,
    optical_transmitter
)

from modules.fiber import (
    apply_attenuation,
    apply_dispersion
)

from modules.receiver import (
    photodetector,
    add_noise,
    sample_signal,
    make_decision
)

from modules.analysis import (
    calculate_ber
)


# ==================================================
# 1. SIMULATION PARAMETERS
# ==================================================

NUM_BITS = 10000

BIT_RATE = 10e9

SAMPLES_PER_BIT = 50

P_LOW = 0.1e-3
P_HIGH = 1.0e-3

ATTENUATION_DB_PER_KM = 0.2

FIBER_LENGTH_KM = 50

DISPERSION_SIGMA = 12

RESPONSIVITY = 0.8

NOISE_STD = 0.03e-3

RANDOM_SEED = 42


# ==================================================
# 2. TIME PARAMETERS
# ==================================================

BIT_DURATION = (
    1 / BIT_RATE
)

DT = (
    BIT_DURATION
    / SAMPLES_PER_BIT
)


# ==================================================
# 3. GENERATE BINARY DATA
# ==================================================

bits = generate_bits(
    NUM_BITS,
    seed=RANDOM_SEED
)


# ==================================================
# 4. CREATE NRZ SIGNAL
# ==================================================

nrz_signal = create_nrz(
    bits,
    SAMPLES_PER_BIT
)


# ==================================================
# 5. CREATE TIME AXIS
# ==================================================

total_samples = len(
    nrz_signal
)

time = (
    np.arange(total_samples)
    * DT
)


# ==================================================
# 6. OPTICAL TRANSMITTER
# ==================================================

optical_power_tx = (
    optical_transmitter(
        nrz_signal,
        P_LOW,
        P_HIGH
    )
)


# ==================================================
# 7. FIBER ATTENUATION
# ==================================================

optical_power_rx, transmission_factor = (
    apply_attenuation(
        optical_power_tx,
        ATTENUATION_DB_PER_KM,
        FIBER_LENGTH_KM
    )
)


# ==================================================
# 8. SIMPLIFIED DISPERSION
# ==================================================

optical_power_dispersed = (
    apply_dispersion(
        optical_power_rx,
        DISPERSION_SIGMA
    )
)


# ==================================================
# 9. PHOTODETECTOR
# ==================================================

photocurrent = (
    photodetector(
        optical_power_dispersed,
        RESPONSIVITY
    )
)


# ==================================================
# 10. ADD RECEIVER NOISE
# ==================================================

noisy_photocurrent = (
    add_noise(
        photocurrent,
        NOISE_STD
    )
)


# ==================================================
# 11. SAMPLE RECEIVED SIGNAL
# ==================================================

received_samples = (
    sample_signal(
        noisy_photocurrent,
        NUM_BITS,
        SAMPLES_PER_BIT
    )
)


# ==================================================
# 12. CALCULATE DECISION THRESHOLD
# ==================================================

I_LOW = (
    RESPONSIVITY
    * P_LOW
    * transmission_factor
)

I_HIGH = (
    RESPONSIVITY
    * P_HIGH
    * transmission_factor
)

THRESHOLD = (
    I_LOW + I_HIGH
) / 2


# ==================================================
# 13. RECEIVER DECISION
# ==================================================

received_bits = (
    make_decision(
        received_samples,
        THRESHOLD
    )
)


# ==================================================
# 14. BER CALCULATION
# ==================================================

errors, ber = (
    calculate_ber(
        bits,
        received_bits
    )
)


# ==================================================
# 15. DISPLAY RESULTS
# ==================================================

print("\n===================================")
print("HIGH-SPEED OPTICAL LINK SIMULATION")
print("===================================\n")

print(
    "Bit Rate:",
    BIT_RATE / 1e9,
    "Gbps"
)

print(
    "Number of Bits:",
    NUM_BITS
)

print(
    "Fiber Length:",
    FIBER_LENGTH_KM,
    "km"
)

print(
    "Dispersion Sigma:",
    DISPERSION_SIGMA
)

print(
    "Noise Standard Deviation:",
    NOISE_STD * 1e3,
    "mA"
)

print(
    "Transmission Factor:",
    round(transmission_factor, 5)
)

print(
    "Bit Errors:",
    errors
)

print(
    "BER:",
    f"{ber:.6e}"
)


# ==================================================
# 16. PLOT FIRST FEW BITS
# ==================================================

PLOT_BITS = 10

plot_samples = (
    PLOT_BITS
    * SAMPLES_PER_BIT
)


plt.figure(figsize=(10, 5))

plt.plot(
    time[:plot_samples] * 1e9,
    noisy_photocurrent[:plot_samples] * 1e3,
    label="Received Noisy Signal"
)

plt.axhline(
    THRESHOLD * 1e3,
    linestyle="--",
    label="Decision Threshold"
)

plt.title(
    "Received Optical Communication Signal"
)

plt.xlabel("Time (ns)")

plt.ylabel("Photocurrent (mA)")

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()
