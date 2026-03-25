import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10, 10, 1000)

def softplus(x):
    return np.log1p(np.exp(x))

y = softplus(x)

plt.figure(figsize=(8,5))
plt.plot(x, y, label="Softplus")
plt.title("Función de activación: Softplus")
plt.xlabel("x")
plt.ylabel("Softplus(x)")
plt.grid(True)
plt.legend()
plt.show()