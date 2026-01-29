import os

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axis
fig, ax = plt.subplots(figsize=(20, 6))  # Changed width from 10 to 20

# Generate square wave data (50% duty cycle)
time = np.linspace(0, 6, 3000)  # Changed back to 6 seconds for 6 cycles
voltage = np.where((time % 1) < 0.5, 0, 3.3)  # Start at low value (0)

# Plot the square wave
ax.plot(time, voltage, linewidth=2, color='blue')

# Add bracket for one cycle (from t=0.5 to t=1.5)
cycle_start, cycle_end = 0.5, 1.5  # Changed to start at the rising edge
bracket_y = -0.5

# Draw bracket lines
ax.plot([cycle_start, cycle_start], [bracket_y - 0.2, bracket_y + 0.2], 'k-', linewidth=1.5)
ax.plot([cycle_start, cycle_end], [bracket_y, bracket_y], 'k-', linewidth=1.5)
ax.plot([cycle_end, cycle_end], [bracket_y - 0.2, bracket_y + 0.2], 'k-', linewidth=1.5)

# Add label for cycle
ax.text((cycle_start + cycle_end) / 2, bracket_y - 0.2, 'One Cycle',  # Moved up closer to the bracket
    ha='center', va='top', fontsize=14)  # Increased font size to 14

# Set labels and limits
ax.set_xlabel('Time (ns)', fontsize=12)
ax.set_ylabel('Voltage (V)', fontsize=12)
ax.set_ylim(-1.2, 3.8)
ax.set_xlim(-0.1, 6.1)  # Changed to show all six cycles
ax.grid(True, alpha=0.3)

# Save figure
fig.savefig(os.path.join(os.path.dirname(__file__), '../img/fig-square-wave-50-percent-duty.png'), dpi=150, bbox_inches='tight')
plt.close()

# Generate square wave data (15% duty cycle)
time_15 = np.linspace(0, 6, 3000)  # Same time for 6 cycles
voltage_15 = np.where(((time_15 - 0.5) % 1) < 0.15, 3.3, 0)  # Shift high period to start at t=0.5s

# Plot the square wave for 15% duty cycle
fig_15, ax_15 = plt.subplots(figsize=(20, 6))  # Same dimensions
ax_15.plot(time_15, voltage_15, linewidth=2, color='red')  # Different color for distinction

# Add bracket for one cycle (from t=0.5 to t=1.5)
cycle_start_15, cycle_end_15 = 0.5, 1.5  # Match bracket position to first figure
bracket_y_15 = -0.5

# Draw bracket lines for the second figure
ax_15.plot([cycle_start_15, cycle_start_15], [bracket_y_15 - 0.2, bracket_y_15 + 0.2], 'k-', linewidth=1.5)
ax_15.plot([cycle_start_15, cycle_end_15], [bracket_y_15, bracket_y_15], 'k-', linewidth=1.5)
ax_15.plot([cycle_end_15, cycle_end_15], [bracket_y_15 - 0.2, bracket_y_15 + 0.2], 'k-', linewidth=1.5)

# Add label for cycle in the second figure
ax_15.text((cycle_start_15 + cycle_end_15) / 2, bracket_y_15 - 0.2, 'One Cycle', 
    ha='center', va='top', fontsize=14)  # Same font size as the first figure

# Set labels and limits for the second figure
ax_15.set_xlabel('Time (ns)', fontsize=12)
ax_15.set_ylabel('Voltage (V)', fontsize=12)
ax_15.set_ylim(-1.2, 3.8)
ax_15.set_xlim(-0.1, 6.1)  # Same limits
ax_15.grid(True, alpha=0.3)

# Save second figure
fig_15.savefig(os.path.join(os.path.dirname(__file__), '../img/fig-square-wave-15-percent-duty.png'), dpi=150, bbox_inches='tight')
plt.close(fig_15)