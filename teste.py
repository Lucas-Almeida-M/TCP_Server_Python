
import numpy as np
import matplotlib.pyplot as plt

# Parameters
Vp = 1  # Peak amplitude in volts
f = 1   # Frequency in Hz
num_samples = 64

# Time array
t = np.linspace(0, 1, num_samples, endpoint=False)  # Assuming one second duration

# Sinusoidal signal
sinusoidal_signal = Vp * np.sin(2 * np.pi * f * t + (2*np.pi/3))



print (sinusoidal_signal + 1)

plt.plot(t, sinusoidal_signal+1, marker='o')
plt.title('Sinusoidal Signal')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.show()