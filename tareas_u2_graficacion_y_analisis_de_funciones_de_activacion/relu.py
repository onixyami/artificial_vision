import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)

def relu(x):
    return np.maximum(0, x)

y = relu(x)

plt.figure(figsize=(8,5))
plt.plot(x, y, label="ReLU")
plt.title("Función de activación: ReLU")
plt.xlabel("x")
plt.ylabel("ReLU(x)")
plt.grid(True)
plt.legend()
plt.show()