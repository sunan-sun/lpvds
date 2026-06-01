import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines
from matplotlib.ticker import MaxNLocator
import random


plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "font.size": 30
})



def plot_ds(x_train, x_test_list, lpvds, *args):
    N = x_train.shape[1]
    if N == 2:
        plot_ds_2d(x_train, x_test_list, lpvds, *args)
    elif N == 3:
        plot_ds_3d(x_train, x_test_list)
    



def plot_ds_2d(x_train, x_test_list, lpvds, *args):
    """ passing lpvds object to plot the streamline of DS (only in 2D)"""
    A = lpvds.A
    att = lpvds.x_att

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot()

    ax.scatter(x_train[:, 0], x_train[:, 1], color='k', s=5, label='original data')
    for idx, x_test in enumerate(x_test_list):
        ax.plot(x_test[:, 0], x_test[:, 1], color= 'r', linewidth=2)

    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    plot_sample = 50
    x_mesh,y_mesh = np.meshgrid(np.linspace(x_min,x_max,plot_sample),np.linspace(y_min,y_max,plot_sample))
    X = np.vstack([x_mesh.ravel(), y_mesh.ravel()])
    gamma = lpvds.damm.compute_gamma(X.T)
    for k in np.arange(len(A)):
        if k == 0:
            dx = gamma[k].reshape(1, -1) * (A[k] @ (X - att.T))  # gamma[k].reshape(1, -1): [1, num] dim x num
        else:
            dx +=  gamma[k].reshape(1, -1) * (A[k] @ (X - att.T)) 
    u = dx[0,:].reshape((plot_sample,plot_sample))
    v = dx[1,:].reshape((plot_sample,plot_sample))

    plt.streamplot(x_mesh,y_mesh,u,v, density=3.0, color="black", arrowsize=1.1, arrowstyle="->")
    # plt.gca().set_aspect('equal')


    if len(args) !=0:
        ax.set_title(args[0])


def plot_ds_3d(x_train, x_test_list):
    N = x_train.shape[1]

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(x_train[:, 0], x_train[:, 1], x_train[:, 2], 'o', color='k', s=3, alpha=0.4, label="Demonstration")

    for idx, x_test in enumerate(x_test_list):
        ax.plot(x_test[:, 0], x_test[:, 1], x_test[:, 2], color= 'b')
    ax.set_xlabel(r'$\xi_1$', fontsize=38, labelpad=20)
    ax.set_ylabel(r'$\xi_2$', fontsize=38, labelpad=20)
    ax.set_zlabel(r'$\xi_3$', fontsize=38, labelpad=20)
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.zaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.tick_params(axis='z', which='major', pad=15)
    ax.axis('equal')
    ax.view_init(elev=30, azim=-20)




def plot_gamma(gamma_arr, **argv):

    M, K = gamma_arr.shape


    colors = ["r", "g", "b", "k", 'c', 'm', 'y', 'crimson', 'lime'] + [
    "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(200)]

    if K == 1:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))

        ax.scatter(np.arange(M), gamma_arr[:, 0], s=5, color=colors[0])
        ax.set_ylim([0, 1])
        if "title" in argv:
            ax.set_title(argv["title"])
        else:
            ax.set_title(r"$\gamma(\cdot)$ over Time")
    else:
        fig, axs = plt.subplots(K, 1, figsize=(12, 8))

        for k in range(K):
            axs[k].scatter(np.arange(M), gamma_arr[:, k], s=5, color=colors[k])
            axs[k].set_ylim([0, 1])
        
        if "title" in argv:
            axs[0].set_title(argv["title"])
        else:
            axs[0].set_title(r"$\gamma(\cdot)$ over Time")


