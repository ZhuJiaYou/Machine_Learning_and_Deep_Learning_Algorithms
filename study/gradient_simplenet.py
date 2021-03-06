import sys, os
import numpy as np

from common.funcs import cross_entropy_error, softmax
from common.gradient import numerical_gradient


class SimpleNet:
    def __init__(self):
        self.w = np.random.randn(2, 3)

    def predict(self, x):
        return np.dot(x, self.w)

    def loss(self, x, t):
        z = self.predict(x)
        y = softmax(z)
        loss = cross_entropy_error(y, t)

        return loss


if __name__ == '__main__':
    x = np.array([0.6, 0.9])
    t = np.array([0, 0, 1])
    net = SimpleNet()

    f = lambda w: net.loss(x, t)
    dw = numerical_gradient(f, net.w)
    print(dw)
