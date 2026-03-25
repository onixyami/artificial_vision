import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)

def tanh(x):
    return np.tanh(x)

y = tanh(x)

plt.figure(figsize=(8,5))
plt.plot(x, y, label="Tanh")
plt.title("Función de activación: Tanh")
plt.xlabel("x")
plt.ylabel("Tanh(x)")
plt.grid(True)
plt.legend()
plt.show()