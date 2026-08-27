import numpy as np
import matplotlib.pyplot as plt

# Reproducibility
np.random.seed(42)

# Number of bits to transmit
num_bits = 20

# Generate random binary data
bits = np.random.randint(0, 2, num_bits)

# Display the generated bits
print("Transmitted Binary Data:")
print(bits)

# Plot the bits
plt.figure(figsize=(10, 3))
plt.step(
    np.arange(num_bits),
    bits,
    where="post"
)

plt.title("Random Binary Data")
plt.xlabel("Bit Index")
plt.ylabel("Bit Value")
plt.yticks([0, 1])
plt.grid(True)

plt.tight_layout()
plt.show()
