import numpy as np
import matplotlib.pyplot as plt

from src.util import load_tools
from src.lpvds_class import lpvds_class

from src.damm.src.util.plot_tools import plot_gmm
from src.util.plot_tools import plot_ds, plot_gamma


if __name__ == "__main__":
    '''
    Choose a data input option:
    1. PC-GMM benchmark data
    2. LASA benchmark data
    3. Damm demo data
    4. DEMO
    '''

    x, x_dot, x_att, x_init = load_tools.load_data(1)


    # run lpvds
    lpvds = lpvds_class(x, x_dot, x_att)
    lpvds.begin()


    # evaluate results
    x_test_list = []
    for x_0 in x_init:
        x_test, gamma_test = lpvds.sim(x_0, dt=0.01)
        x_test_list.append(x_test)


    # plot results
    plot_gmm(x, lpvds.assignment_arr, lpvds.damm)
    plot_ds(x, x_test_list, lpvds)
    plot_gamma(gamma_test)
    plt.show()
