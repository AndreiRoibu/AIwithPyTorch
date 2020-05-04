# -*- coding: utf-8 -*-
"""Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zXA0ykqa36PwJQrOS6Hj5wjNHXG1exoL
"""

import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# We make the dataset

N = 1000
X = np.random.random((N, 2)) * 6 -3 # uniform distribution in [-3, 3]
y = np.cos(2 * X[:,0]) + np.cos(3 * X[:,1])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], y)
plt.show()

model = nn.Sequential(
    nn.Linear(2,128),
    nn.ReLU(),
    nn.Linear(128, 1)
)

Loss = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

def train_model(model, Loss, optimizer, X_train, y_train, epochs=1000):
    train_losses = np.zeros(epochs)
    for iteration in range(epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = Loss(outputs, y_train)
        loss.backward()
        optimizer.step()
        train_losses[iteration] = loss.item()
        if (iteration+1) % 50 == 0:
            print("Epoch: {}/{}, Train Loss: {}".format(iteration+1, epochs, loss.item()))

    return train_losses

X_train = torch.from_numpy(X.astype(np.float32))
y_train = torch.from_numpy(y.astype(np.float32).reshape(-1, 1))
train_losses = train_model(model, Loss, optimizer, X_train, y_train)

plt.plot(train_losses)

#Plot the predicted surface

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], y)

with torch.no_grad():
    line = np.linspace(-3, 3, 50)
    xx, yy = np.meshgrid(line, line)
    Xgrid = np.vstack((xx.flatten(), yy.flatten())).T
    Xgrid_torch = torch.from_numpy(Xgrid.astype(np.float32))
    Yhat = model(Xgrid_torch).numpy().flatten()
    ax.plot_trisurf(Xgrid[:, 0], Xgrid[:,1], Yhat, linewidth=0.2, antialiased=True)
    plt.show()

#Test interpolation 

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0], X[:,1], y)

with torch.no_grad():
    line = np.linspace(-5, 5, 50)
    xx, yy = np.meshgrid(line, line)
    Xgrid = np.vstack((xx.flatten(), yy.flatten())).T
    Xgrid_torch = torch.from_numpy(Xgrid.astype(np.float32))
    Yhat = model(Xgrid_torch).numpy().flatten()
    ax.plot_trisurf(Xgrid[:, 0], Xgrid[:,1], Yhat, linewidth=0.2, antialiased=True)
    plt.show()

