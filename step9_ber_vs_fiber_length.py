import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Simulation parameters
# --------------------------------------------------

np.random.seed(42)

num_bits = 100000

# Optical transmitter
P_low = 0.1e-3
P_high = 1.0e-3

# Photodetector
responsivity = 0.8  # A/W

# Fiber
attenuation_db_per_km = 0.2

# Receiver noise
noise_std = 0.05e-3  # A


# --------------------------------------------------
# 2. Generate random transmitted bits
# --------------------------------------------------

bits = np.random.randint(
    0,
    2,
    num_bits
)


# --------------------------------------------------
# 3. Define fiber lengths
# --------------------------------------------------

fiber_lengths_km = np.linspace(
    0,
    100,
    21
)


# --------------------------------------------------
# 4. Store BER values
# --------------------------------------------------

ber_values = []

received_power_values = []


# --------------------------------------------------
# 5. Run simulation for each fiber length
# --------------------------------------------------

for fiber_length_km in fiber_lengths_km:

    # Total fiber loss in dB
    total_loss_db = (
        attenuation_db_per_km
        * fiber_length_km
    )

    # Power transmission factor
    transmission_factor = 10 ** (
        -total_loss_db / 10
    )

    # Received optical power levels
    P_low_rx = (
        P_low
        * transmission_factor
    )

    P_high_rx = (
        P_high
        * transmission_factor
    )

    # Convert optical power to photocurrent
    I_low = (
        responsivity
        * P_low_rx
    )

    I_high = (
        responsivity
        * P_high_rx
    )

    # Create clean received signal
    clean_current = (
        I_low
        + (I_high - I_low) * bits
    )

    # Add Gaussian noise
    noise = np.random.normal(
        loc=0,
        scale=noise_std,
        size=num_bits
    )

    noisy_current = (
        clean_current + noise
    )

    # Decision threshold
    threshold = (
        I_low + I_high
    ) / 2

    # Recover bits
    received_bits = (
        noisy_current > threshold
    ).astype(int)

    # Calculate errors
    errors = np.sum(
        bits != received_bits
    )

    # Calculate BER
    ber = errors / num_bits

    # Store results
    ber_values.append(ber)

    received_power_values.append(
        P_high_rx
    )

    # Display result
    print(
        f"Fiber Length: {fiber_length_km:.1f} km | "
        f"BER: {ber:.6f}"
    )


# --------------------------------------------------
# 6. Convert lists to NumPy arrays
# --------------------------------------------------

ber_values = np.array(ber_values)

received_power_values = np.array(
    received_power_values
)


# --------------------------------------------------
# 7. Plot BER vs Fiber Length
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.semilogy(
    fiber_lengths_km,
    ber_values,
    marker="o"
)

plt.title("BER vs Fiber Length")

plt.xlabel("Fiber Length (km)")

plt.ylabel("Bit Error Rate (BER)")

plt.grid(True, which="both")

plt.tight_layout()

plt.show()


# --------------------------------------------------
# 8. Plot Received Power vs Fiber Length
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.plot(
    fiber_lengths_km,
    received_power_values * 1e3,
    marker="o"
)

plt.title("Received Optical Power vs Fiber Length")

plt.xlabel("Fiber Length (km)")

plt.ylabel("Maximum Received Optical Power (mW)")

plt.grid(True)

plt.tight_layout()

plt.show()