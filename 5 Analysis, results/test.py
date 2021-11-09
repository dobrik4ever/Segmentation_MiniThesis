import numpy as np

a = np.random.random((3, 3, 3))
print(a)


def plot_3d(a):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(a[0], a[1], a[2])
    plt.show()

plot_3d(a)