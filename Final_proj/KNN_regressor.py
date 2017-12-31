import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors

def preprocessing():
    df = pd.read_csv('car.csv')

    #delete unnecessary data columns
    df = df.drop(df.index[[0]]) #drop the label, say the first row , NOT IN PLACE
    del df['body_type']
    del df['color_slug']
    del df['stk_year']
    del df['date_created']
    del df['date_last_seen']
    df = df.dropna() #drop row with na value, NOT IN PLACE

    print(df)
    #new_df = df[df['maker']=='ford']
    #print(new_df)
    #new_df2 = df[df['maker']=='skoda']
    #print(new_df2)
    return df
def draw_PDF(df): #draw the pdf of each column
    df.values.tolist()
    df = np.array(df)
    for i in range(len(df[0])):
        tf = df[:,i]
        print("tf be like ",tf)
        tf.sort()
        weight_percent = np.ones_like(tf)/float(len(tf))
        plt.title(f' feature {i+1}: PDF')
        plt.tight_layout()
        plt.savefig(f' feature {i+1}: PDF',dpi=600)

if __name__ == '__main__':
    draw_PDF(preprocessing())
