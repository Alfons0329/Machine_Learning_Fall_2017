import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('train.csv')
data = np.array(df).T

for i in range(len(data)):
    a = np.hstack(data[i])

    plt.figure()
    plt.hist(a, bins = 'auto', normed = True )
    plt.title(f'Forestfire feature{i+1}: FFMC Probability Distribution Function')
    plt.show()
