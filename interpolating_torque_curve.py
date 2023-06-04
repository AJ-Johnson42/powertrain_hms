import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

# Simulated torque for the modified engine
modified_simulated = np.array([
    [5000.0, 40.309258],
    [5500.0, 41.44008],
    [6000.0, 42.912045],
    [6500.0, 44.15846],
    [7000.0, 45.307384],
    [7500.0, 44.26793],
    [8000.0, 43.260014],
    [8500.0, 44.893463],
    [9000.0, 44.735756],
    [9500.0, 46.28183],
    [10000.0, 46.433773],
    [10500.0, 45.448467],
    [11000.0, 43.33842],
    [11500.0, 40.59386],
    [12000.0, 37.902637],
    [12500.0, 35.37],
    [13000.0, 33.05923],
])

# Simulated torque for the stock engine
stock_simulated = np.array([
    [5000.0, 35.720577],
    [5500.0, 37.444637],
    [6000.0, 37.679615],
    [6500.0, 39.630043],
    [7000.0, 40.03528],
    [7500.0, 38.573265],
    [8000.0, 37.033257],
    [8500.0, 37.79023],
    [9000.0, 38.391075],
    [9500.0, 38.45455],
    [10000.0, 39.946106],
    [10500.0, 41.079266],
    [11000.0, 41.241932],
    [11500.0, 39.64086],
    [12000.0, 37.37364],
    [12500.0, 34.996933],
    [13000.0, 32.817066],
])

# Experimental/known values for the stock engine
stock_experimental = np.array([
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


stock_experimental_cs = CubicSpline(stock_experimental[:, 0], stock_experimental[:, 1])
stock_simulated_cs = CubicSpline(stock_simulated[:, 0], stock_simulated[:, 1])
rpm_values = np.arange(5000, 13001, 500)
stock_experimental_torque = stock_experimental_cs(rpm_values)
stock_simulated_torque = stock_simulated_cs(rpm_values)
torque_ratio = stock_experimental_torque / stock_simulated_torque
modified_simulated_cs = CubicSpline(modified_simulated[:, 0], modified_simulated[:, 1])
modified_simulated_torque = modified_simulated_cs(rpm_values)
modified_experimental_torque = modified_simulated_torque * torque_ratio
print(np.column_stack((rpm_values, modified_experimental_torque)))


plt.figure(figsize=(10, 6))
plt.plot(rpm_values, modified_experimental_torque, label="Modified Engine Estimated Experimental Torque", linestyle="--")
plt.plot(modified_simulated[:, 0], modified_simulated[:, 1], label="Modified Engine Simulated Torque")
plt.plot(stock_simulated[:, 0], stock_simulated[:, 1], label="Stock Engine Simulated Torque")
plt.scatter(stock_experimental[:, 0], stock_experimental[:, 1], label="Stock Engine Experimental Torque", color="red")

plt.xlabel("RPM")
plt.ylabel("Torque (ft-lb)")
plt.title("Engine Torque vs RPM")
plt.legend()
plt.grid(True)
plt.show()
