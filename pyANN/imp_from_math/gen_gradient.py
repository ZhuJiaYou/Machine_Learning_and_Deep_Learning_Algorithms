"""gen_gradient.py
------------------
Use network2 to figure out the average starting values of the gradient error terms
\delta^l_j = \partial c / \partial z^l_j = \partial c / \partial b^l_j
"""
import json
import math
import random
import shutil  # 高级的文件、文件夹、压缩包等处理模块
import sys
from functools import reduce

import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import mnist_loader
import network2


def main():
    full_training_data, _, _ = mnist_loader.load_data_wrapper()
    training_data = full_training_data[:1000]
    epoches = 500

    print("\nTwo hidden layers:")
    net = network2.Network([784, 30, 30, 10])
    initial_norms(training_data, net)
    abbreviated_gradient = [ag[:6] for ag in get_average_gradient(net, training_data)[:-1]]
    print("Saving the averaged gradient for the top six nerons in each layer.")
    with open("./js/initial_gradient.json", "w") as f:
        json.dump(abbreviated_gradient, f)
    training(training_data, net, epoches, "./js/norms_during_training_2_layers.json")
    plot_training(epoches, "./js/norms_during_training_2_layers.json", 2)

    print("\nThree hidden layers:")
    net = network2.Network([784, 30, 30, 30, 10])
    initial_norms(training_data, net)
    training(training_data, net, epoches, "./js/norms_during_training_3_layers.json")
    plot_training(epoches, "./js/norms_during_training_3_layers.json", 3)

    print("\nFour hidden layers:")
    net = network2.Network([784, 30, 30, 30, 30, 10])
    initial_norms(training_data, net)
    training(training_data, net, epoches, "./js/norms_during_training_4_layers.json")
    plot_training(epoches, "./js/norms_during_training_4_layers.json", 4)


def initial_norms(training_data, net):
    average_gradient = get_average_gradient(net, training_data)
    norms = [list_norm(avg) for avg in average_gradient[:-1]]
    print("Average gradient forthe hidden layers: " + str(norms))


def get_average_gradient(net, training_data):
    nabla_b_results = [net.backprop(x, y)[0] for (x, y) in training_data]
    gradient = list_sum(nabla_b_results)
    return [(np.reshape(g, len(g)) / len(training_data)).tolist() for g in gradient]


def training(training_data, net, epoches, filename):
    norms = []
    for j in range(epoches):
        average_gradient = get_average_gradient(net, training_data)
        norms.append([list_norm(avg) for avg in average_gradient[:-1]])
        print("Epoch: {}".format(j))
        net.SGD(training_data, 1, 1000, 0.1, lmbda=5.0)
    with open(filename, "w") as f:
        json.dump(norms, f)


def zip_sum(a, b):
    return [x + y for (x, y) in zip(a, b)]


def list_sum(l):
    return reduce(zip_sum, l)


def list_norm(l):
    return math.sqrt(sum([x * x for x in l]))


def plot_training(epoches, filename, num_layers):
    with open(filename, "r") as f:
        norms = json.load(f)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    colors = ["#2A6EA6", "#FFA933", "#FF5555", "#55FF55", "#5555FF"]
    for j in range(num_layers):
        ax.plot(np.arange(epoches), [n[j] for n in norms], color=colors[j], 
                label='Hidden layer {}'.format(j + 1))
    ax.grid(True)
    ax.set_xlim([0, epoches])
    ax.set_xlabel('Epoch')
    ax.set_title("Speed of learning: {} hidden layers".format(num_layers))
    ax.set_yscale('log')
    plt.legend(loc='upper right')
    fig_filename = "training_speed_{}_layers.png".format(num_layers)
    plt.savefig('./figs/{}'.format(fig_filename))
    plt.show()


if __name__ == "__main__":
    main()
