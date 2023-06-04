import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Load data from CSV file
data = np.genfromtxt('/Users/aj/Desktop/Git/Motec-Data-Analysis/MockEndurance.csv', delimiter='","', dtype=float, skip_header=18, encoding = 'utf-8')

# Extract data columns
rpm_data = data[:, 26]
throttle_position_data = data[:, 25]
oil_pressure_data = data[:, 33] * 0.145038  # Convert to PSI
steering_angle = data[:, 78]


# Set up RPM bins
rpm_bins = np.arange(3000, 13500, 500)

throttle_bins = np.array([0, 20, 40, 60, 80, 100])
throttle_labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
throttle_categories = np.digitize(throttle_position_data, throttle_bins)
throttle_colors = ListedColormap(['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231'])

rpm_counts = []
for i in range(1, len(throttle_bins)):
    rpm_counts.append(np.histogram(rpm_data[throttle_categories == i], bins=rpm_bins)[0])

# Stacked bar chart setup
fig, ax = plt.subplots()
ax.bar(rpm_bins[:-1], rpm_counts[0], width=500, align='edge', color=throttle_colors(0), edgecolor='black', linewidth=0.5, label=throttle_labels[0])
for i in range(1, len(throttle_bins)-1):
    ax.bar(rpm_bins[:-1], rpm_counts[i], width=500, align='edge', color=throttle_colors(i), edgecolor='black', linewidth=0.5, bottom=np.sum(rpm_counts[:i], axis=0), label=throttle_labels[i])

ax.set_title('Mock Autocrosses: Count vs RPM vs Throttle Position')
ax.set_xlabel('RPM')
ax.set_ylabel('5ms Time Count')
ax.legend(title='Throttle Position')
plt.show()

fig, ax = plt.subplots()
# hb = ax.hexbin(rpm_data, oil_pressure_data, gridsize=30, cmap='inferno', mincnt=1)
hb = ax.hexbin(steering_angle, oil_pressure_data, gridsize=30, cmap='inferno', mincnt=1)

# Add colorbar
cb = fig.colorbar(hb, ax=ax)
cb.set_label('Time Count 5ms')
ax.set_title('Mock Autocrosses: Oil Pressure vs. RPM vs. Time Count')
ax.set_xlabel('RPM')
ax.set_ylabel('Oil Pressure (PSI)')

plt.show()