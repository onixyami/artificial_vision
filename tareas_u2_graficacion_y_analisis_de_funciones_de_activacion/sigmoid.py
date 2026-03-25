import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

y = sigmoid(x)

plt.figure(figsize=(8,5))
plt.plot(x, y, label="Sigmoid")
plt.title("Función de activación: Sigmoid")
plt.xlabel("x")
plt.ylabel("Sigmoid(x)")
plt.grid(True)
plt.legend()
plt.show()
