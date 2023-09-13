from sklearn.linear_model import LinearRegression
import numpy as np
import os
import time
os.system('cls' if os.name == 'nt' else 'clear')


# Seus dados
data = np.array([1,3,7,11,13])

# Reshape seus dados para o formato correto
X = data[:-1].reshape(-1, 1)
Y = data[1:]
print(X)
# Treine o modelo
model = LinearRegression()
model.fit(X, Y)

# Use o modelo para prever os próximos 5 valores
X_future = [[1],[3],[7],[11]]


Y_future = model.predict(X_future)

for i in range(100):
	X_future.append([int(Y_future[-1])])
	Y_future = model.predict(X_future)

print(X_future)
