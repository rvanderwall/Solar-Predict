__author__ = 'robertv'

import numpy as np
import matplotlib.pyplot as plt

def plot_xy_data(X, x_label, y, plot_name):
    plt.plot(X, y, 'rx')

    plt.xlabel(x_label)
    plt.ylabel('solar flux')
    plt.title('Data: ' + plot_name)
    plt.show()

def plot_xy_data_with_fit(dates, y_predict, y_actual, x_label, plot_name):
    X = range(0,dates.shape[0])
    plt.plot(X, y_actual, 'rx')

    plt.plot(X, y_predict)

    plt.xlabel(x_label)
    plt.ylabel('solar flux')
    plt.title('Data: ' + plot_name)
    plt.show()

def plot_elevation_vs_output(elevations, outputs):
    return

def plot_cost_function(J_History, test_name):
    iters = range(0,J_History.shape[0])
    plt.plot(iters, J_History)

    plt.xlabel('iteration')
    plt.ylabel('Cost Function')
    plt.title('Cost function vs Iteration: ' + test_name)
    plt.show()
