import numpy as np
import matplotlib.pyplot as plt

def main():
    data  = np.genfromtxt('../input/data.txt', skip_header = 1)

    with open('../output/tables.txt', 'w') as f:
        f.write('<tab:table>\n')
        f.write('%s\n%.3f\n%d\n%d' % (np.mean(data), np.std(data, ddof = 1), np.max(data), np.min(data)))

    plt.hist(data)
    plt.savefig('../output/plot.eps')

main()
