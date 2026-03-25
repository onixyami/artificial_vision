import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)

def leaky_relu(x, alpha=0.01):
    return np.where(x > 0, x, alpha * x)

y = leaky_relu(x)

plt.figure(figsize=(8,5))
plt.plot(x, y, label="Leaky ReLU")
plt.title("Función de activación: Leaky ReLU")
plt.xlabel("x")
plt.ylabel("LeakyReLU(x)")
plt.grid(True)
plt.legend()
plt.show()
