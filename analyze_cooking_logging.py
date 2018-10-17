import sys

import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv(sys.argv[1])
    df.columns = ['frame', 'predictions']

    X = df['frame']
    Y = df['predictions']
    plt.figure()
    plt.plot(X, Y)
    plt.show()

    # each 100 counts
    start = 0
    end = 50
    for i in range(300):
        print(i*30)
        plt.plot(X[start:end], Y[start:end])
        plt.ylim(0.0, 8.0)
        plt.show()

        plt.hist(Y[start:end])
        plt.xlim(0.0, 8.0)
        plt.show()

        start += 100
        end += 100


if __name__ == '__main__':
    main()





