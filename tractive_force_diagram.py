import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

#Legend function for figure
def ordinal_suffix(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

# torque_rpm_data = np.array([
#     [5000.0, 33.85381317],
#     [5500.0, 34.30778298],
#     [6000.0, 34.16599002],
#     [6500.0, 34.54228551],
#     [7000.0, 37.34565293],
#     [7500.0, 40.16713519],
#     [8000.0, 40.88488598],
#     [8500.0, 40.39080318],
#     [9000.0, 40.78425676],
#     [9500.0, 43.32766552],
#     [10000.0, 41.84677796],
#     [10500.0, 37.6162485],
#     [11000.0, 35.7283524],
#     [11500.0, 33.79334808],
#     [12000.0, 32.45293699],
#     [12500.0, 30.31979974],
# ])

torque_rpm_data = np.array([
    [5000, 30],
    [5100, 30],
    [5200, 30],
    [5300, 30],
    [5400, 30],
    [5500, 31],
    [5600, 30],
    [5700, 32],
    [5800, 29],
    [5900, 31],
    [6000, 30],
    [6100, 28],
    [6200, 29],
    [6300, 29],
    [6400, 29],
    [6500, 31],
    [6600, 31],
    [6700, 32],
    [6800, 32],
    [6900, 33],
    [7000, 33],
    [7100, 34],
    [7200, 34],
    [7300, 34],
    [7400, 35],
    [7500, 35],
    [7600, 34],
    [7700, 35],
    [7800, 35],
    [7900, 35],
    [8000, 35],
    [8100, 35],
    [8200, 35],
    [8300, 34],
    [8400, 36],
    [8500, 34],
    [8600, 35],
    [8700, 35],
    [8800, 35],
    [8900, 34],
    [9000, 35],
    [9100, 35],
    [9200, 33],
    [9300, 34],
    [9400, 35],
    [9500, 36],
    [9600, 36],
    [9700, 35],
    [9800, 35],
    [9900, 36],
    [10000, 36],
    [10100, 35],
    [10200, 35],
    [10300, 35],
    [10400, 35],
    [10500, 34],
    [10600, 34],
    [10700, 34],
    [10800, 33],
    [10900, 34],
    [11000, 34],
    [11100, 34],
    [11200, 33],
    [11300, 33],
    [11400, 33],
    [11500, 33],
    [11600, 34],
    [11700, 33],
    [11800, 33],
    [11900, 33],
    [12000, 32],
    [12100, 32],
    [12200, 32],
    [12300, 31],
    [12400, 30],
    [12500, 30],
    [12600, 30],
    [12700, 29],
    [12800, 29],
])

rpm = torque_rpm_data[:, 0]
torque_ftlb = torque_rpm_data[:, 1]
torque = torque_ftlb * 1.35582

gear_ratios = np.array([
    [1, 2.846],
    [2, 2.200],
    [3, 1.850],
    [4, 1.600],
    [5, 1.421],
    [6, 1.300],
])

final_drive_ratio = 2.9
primary_reduction_ratio = 1.9
gear_ratios = gear_ratios[:, 1] * final_drive_ratio * primary_reduction_ratio

wheel_radius_ft = 0.667
wheel_radius_meters = wheel_radius_ft * 0.3048 #to meters
wheel_diameter_inches = wheel_radius_ft * 2 * 12
tire_diameter_in = wheel_diameter_inches

# Max force traction
mass_car = (480+150) * 0.453592 #kg
max_experimental_accel = 1.3  * 9.81 #m/s^2

max_force_traction = mass_car * max_experimental_accel
print(max_force_traction)

tractive_forces = [torque * gear_ratio / wheel_radius_meters for gear_ratio in gear_ratios]
        
wheel_rpms = [[rpm_value / (gear_ratio) for rpm_value in rpm] for gear_ratio in gear_ratios]
ground_speeds_mph = [[(wheel_rpm * tire_diameter_in * np.pi * 60 / 63360) for wheel_rpm in wheel_rpms_gear] for wheel_rpms_gear in wheel_rpms]

#Flat power curve
power = torque * rpm * 2 * np.pi / 60
max_power = np.max(power)
flat_power_curve = np.full_like(rpm, max_power)

#Figure setup
plt.figure(figsize=(10, 6))
tangent_points = []

# #Plot tractive force vs ground speed for each gear
# for gear in range(len(gear_ratios)):
#     plt.plot(ground_speeds_mph[gear], tractive_forces[gear], label=f'{gear + 1}st Gear')
#     max_force_index = np.argmax(tractive_forces[gear])
#     tangent_points.append((ground_speeds_mph[gear][max_force_index], tractive_forces[gear][max_force_index]))

# ...

# Plot tractive force vs ground speed for each gear
for gear in range(len(gear_ratios)):
    gear_num = gear + 1
    gear_label = ordinal_suffix(gear_num)
    plt.plot(ground_speeds_mph[gear], tractive_forces[gear], label=f'{gear_label} Gear')

# ...


tangent_points = np.array(tangent_points)

# # Flat power curve
# x_tangent = tangent_points[:, 0]
# y_tangent = tangent_points[:, 1]
# cs = CubicSpline(x_tangent, y_tangent)

# x_flat_power = np.linspace(x_tangent.min(), x_tangent.max(), 1000)
# y_flat_power = cs(x_flat_power)

# plt.plot(x_flat_power, y_flat_power, '--', label='Flat Power Curve')

#plot max force traction
plt.plot(np.linspace(10,45,35), np.full_like(np.linspace(10,45,35), max_force_traction), '--', label='Max Traction Force')

plt.xlabel('Ground Speed (mph)')
plt.ylabel('Tractive Force (N)')
plt.title('Tractive Force vs Longitudinal Ground Speed')
plt.legend()
plt.grid(True)

plt.show()