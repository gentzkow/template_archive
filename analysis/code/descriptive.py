import numpy as np
import matplotlib.pyplot as plt

def main():
    data = np.genfromtxt('input/data_graph.txt', skip_header = 1)

    plt.hist(data)
    plt.savefig('output/plot.eps')

# EXECUTE
main()