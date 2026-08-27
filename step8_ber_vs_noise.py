import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Simulation parameters
# --------------------------------------------------

np.random.seed(42)

num_bits = 100000

bit_rate = 10e9

P_low = 0.1e-3
P_high = 1.0e-3

responsivity = 0.8

attenuation_db_per_km = 0.2
fiber_length_km = 10


# --------------------------------------------------
# 2. Calculate fiber transmission
# --------------------------------------------------

total_loss_db = (
    attenuation_db_per_km
    * fiber_length_km
)

transmission_factor = 10 ** (
    -total_loss_db / 10
)


# --------------------------------------------------
# 3. Calculate received current levels
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


# --------------------------------------------------
# 4. Calculate decision threshold
# --------------------------------------------------

threshold = (
    I_low + I_high
) / 2


# --------------------------------------------------
# 5. Generate random bits
# --------------------------------------------------

bits = np.random.randint(
    0,
    2,
    num_bits
)


# --------------------------------------------------
# 6. Convert bits to photocurrent levels
# --------------------------------------------------

clean_current = (
    I_low
    + (I_high - I_low) * bits
)


# --------------------------------------------------
# 7. Define different noise levels
# --------------------------------------------------

noise_std_values = np.linspace(
    0.01e-3,
    0.30e-3,
    20
)


# --------------------------------------------------
# 8. Store BER results
# --------------------------------------------------

ber_values = []


# --------------------------------------------------
# 9. Run simulation for each noise level
# --------------------------------------------------

for noise_std in noise_std_values:

    # Generate Gaussian noise
    noise = np.random.normal(
        loc=0,
        scale=noise_std,
        size=num_bits
    )

    # Add noise to signal
    noisy_current = (
        clean_current + noise
    )

    # Receiver decision
    received_bits = (
        noisy_current > threshold
    ).astype(int)

    # Calculate number of errors
    errors = np.sum(
        bits != received_bits
    )

    # Calculate BER
    ber = errors / num_bits

    # Store BER
    ber_values.append(ber)

    print(
        "Noise:",
        round(noise_std * 1e3, 4),
        "mA | BER:",
        ber
    )


# --------------------------------------------------
# 10. Convert results to NumPy array
# --------------------------------------------------

ber_values = np.array(ber_values)


# --------------------------------------------------
# 11. Plot BER vs noise
# --------------------------------------------------

plt.figure(figsize=(8, 5))

plt.semilogy(
    noise_std_values * 1e3,
    ber_values,
    marker="o"
)

plt.title("BER vs Gaussian Noise Standard Deviation")

plt.xlabel(
    "Noise Standard Deviation (mA)"
)

plt.ylabel(
    "Bit Error Rate (BER)"
)

plt.grid(True, which="both")

plt.tight_layout()

plt.show()