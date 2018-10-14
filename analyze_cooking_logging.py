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


if __name__ == '__main__':
    main()
