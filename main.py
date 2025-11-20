import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# USER PARAMETERS
# -----------------------------
n_spots = 10           # number of beam spots per layer
n_layers = 3           # number of energy layers
spot_width = 1.0 / n_spots
x = np.linspace(-1.5, 1.5, 1000)   # high-res space for plotting

# Target motion parameters
A = 0.05      # amplitude of oscillation
T = 7         # breathing period (s)
omega = 2 * np.pi / T
epsilon = np.pi

# Timing
delta_t = 0.2           # delay between spots in same layer (s)
layer_delay = 1.0        # delay between layers (s)

# -----------------------------
# DEFINE SPOT POSITIONS AND WEIGHTS
# -----------------------------
spot_edges = np.linspace(-1, 1, n_spots + 1)
spot_centers = 0.5 * (spot_edges[:-1] + spot_edges[1:])

def F(x):
    """Underlying target function (same for all layers)."""
    return x**2
    #return [1]*len(x)

spot_weights = F(spot_centers)
spot_weights /= np.max(spot_weights)

# -----------------------------
# DEFINE DELIVERY ORDERS
# -----------------------------
orders = {
    "Left → Right": np.arange(n_spots),
    "Right → Left": np.arange(n_spots - 1, -1, -1),
    "Random": np.random.permutation(n_spots),
}

# -----------------------------
# SIMULATION FUNCTION
# -----------------------------
def delivered_profile(order, layer_idx):
    """Compute delivered dose distribution for one layer and order."""
    delivered = np.zeros_like(x)
    base_time = layer_idx * (n_spots * delta_t + layer_delay)

    t = base_time
    prev_idx = order[0]

    print('layer', layer_idx, 'order', order)
    for i, idx in enumerate(order):
        if i > 0:
            jump = abs(idx - prev_idx)
            t += jump * delta_t
        prev_idx = idx
        print(t)
        motion = A * np.sin(omega * t + epsilon)

        left_edge = spot_edges[idx]
        right_edge = spot_edges[idx + 1]

        shifted_left = left_edge - motion
        shifted_right = right_edge - motion

        mask = (x >= shifted_left) & (x < shifted_right)
        delivered[mask] += spot_weights[idx]

    return delivered

# -----------------------------
# COMPUTE AND PLOT RESULTS
# -----------------------------
fig, axes = plt.subplots(n_layers, 1, figsize=(10, 2.5 * n_layers), sharex=True)

if n_layers == 1:
    axes = [axes]

# Intended static dose
intended = np.zeros_like(x)
for i in range(n_spots):
    mask = (x >= spot_edges[i]) & (x < spot_edges[i + 1])
    intended[mask] = spot_weights[i]

# Plot each energy layer independently
for layer_idx, ax in enumerate(axes):
    ax.plot(x, intended, 'k--', lw=2, label="Intended Static F(x)")

    for name, order in orders.items():
        delivered = delivered_profile(order, layer_idx)
        mse = np.mean((delivered - intended)**2)
        ax.plot(x, delivered, lw=2, alpha=0.9,
                label=f"{name} — MSE={mse:.4f}")

    ax.set_title(f"Energy Layer {layer_idx + 1}")
    ax.set_ylabel("Relative Dose")
    ax.grid(True)
    ax.legend()

axes[-1].set_xlabel("Position (normalized 0–1)")
plt.suptitle(f"Multi-Layer Dose Delivery with Motion ({n_layers} layers)", y=0.95)
plt.tight_layout()
plt.show()
