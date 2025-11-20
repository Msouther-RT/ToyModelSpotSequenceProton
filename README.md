# Proton Beam Spot Scanning Motion Simulation

A Python simulation that models the effects of target motion (e.g., breathing) on multi-layer proton beam therapy dose delivery using different spot scanning orders.

## Installation

This project uses `uv` for dependency management. 

### Install uv

Follow the installation instructions at: https://docs.astral.sh/uv/getting-started/installation/

### Setup and Run
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install dependencies
uv sync

# Run the simulation
uv run main.py
```

## What This Code Does

This simulation models proton therapy beam delivery where:

- **Target Motion**: The treatment target (e.g., a tumor in the chest) oscillates sinusoidally to simulate breathing motion
- **Multi-Layer Delivery**: Proton beams are delivered at multiple energy layers to achieve depth coverage
- **Spot Scanning**: Each layer consists of multiple beam spots delivered sequentially
- **Delivery Order Comparison**: Three different spot delivery orders are compared:
  - Left → Right (sequential)
  - Right → Left (reverse sequential)  
  - Random order

The simulation calculates how the moving target causes the actual delivered dose distribution to deviate from the intended static dose pattern. Mean Squared Error (MSE) is computed for each delivery order to quantify the deviation.

## Key Parameters

- `n_spots`: Number of beam spots per energy layer (default: 10)
- `n_layers`: Number of energy layers (default: 3)
- `A`: Amplitude of target oscillation (default: 0.05)
- `T`: Breathing period in seconds (default: 7)
- `delta_t`: Time delay between spots (default: 0.2s)
- `layer_delay`: Time delay between energy layers (default: 1.0s)

## Output

The code generates a multi-panel plot showing:

- Black dashed line: Intended static dose distribution
- Colored lines: Actually delivered dose for each scanning order
- MSE values quantifying the delivery accuracy for each order

This helps visualize how different delivery sequences interact with periodic motion and which strategy minimizes motion-induced dose errors.