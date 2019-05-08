import numpy as np
import matplotlib.pyplot as plt

def main():
    data = np.genfromtxt('input/data_graph.csv', skip_header = 1)

    plt.hist(data)
    plt.savefig('output/plot.eps')
    
    data = np.genfromtxt('input/data_table.csv', skip_header = 1)
    
    with open('output/tables.txt', 'w') as f:
        f.write('<tab:table>\\n'),
        f.write('%s\n%.3f\n%d\n%d' % (np.mean(data), np.std(data, ddof = 1), np.max(data), np.min(data)))

# EXECUTE
main()
