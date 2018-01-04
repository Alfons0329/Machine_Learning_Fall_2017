import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import neighbors
from sklearn import tree 
import scipy.stats as stats

def preprocessing():
    df = pd.read_csv('car.csv')
    
    #delete unnecessary data columns
    df = df.drop(df.index[0]) #drop the label, say the first row , NOT IN PLACE
    del df['body_type']
    del df['color_slug']
    del df['stk_year']
    del df['date_created']
    del df['date_last_seen']
    df = df.dropna() #drop row with na value, NOT IN PLACE
    
    #print(df)
    car_name = df[['maker']]
    car_name.dtypes.value_counts()
    return df

def draw_PDF(df): #draw the pdf of each column
    df = df.mask(df.astype(object).eq('None')).dropna()
    sample_df = df.sample(n=1000)
    
    print(sample_df)
    maker_count = sample_df.groupby(['maker']).size()
    
    year_count = sample_df.groupby(['manufacture_year']).size()
    
    fuel_count = sample_df.groupby(['fuel_type']).size()
    
    sample_df['door_count'] = sample_df['door_count'].astype(int)
    
    door_count = sample_df.groupby(['door_count']).size()
    
    transmission_count = sample_df.groupby(['transmission']).size()
    
    sample_df['seat_count'] = sample_df['seat_count'].astype(int)
    seat_count = sample_df.groupby(['seat_count']).size()
    
    print(seat_count)
    
    pdf = np.array(sample_df)
    #plt.figure()
    
    for i in [2,4,5,10]:
        tdf = pdf[:,i]
        tdf.sort()
        tdf = tdf.tolist()
        print(type(tdf))
        print('sort')
        #mean = np.mean(tdf)
        weights = np.ones_like(tdf)/float(len(tdf))
        print('weight')
        #std = np.std(tdf)
        #pdf = stats.norm.pdf(tdf,mean,std)
        #plt.plot(tdf,pdf)
        if i==2:
            plt.hist(tdf,bins=list(range(0,400000,20000)),weights=weights)
        elif i==10:
            plt.hist(tdf,bins=list(range(0,150000,5000)),weights=weights)
        else:
            plt.hist(tdf,weights=weights)
        print('hist')
        plt.tight_layout()
        plt.show()
    
    makers = maker_count.keys()
    maker_list = []
    count_list = []
    summ = 0
    for i in range(len(makers)):
        maker_list.append(makers[i])
        count_list.append(maker_count[i])
        summ = summ + maker_count[i]
        
    years = year_count.keys()
    year_count = year_count.tolist()
    #print(years)
    year_list = []
    year_count_list = []
    year_sum = 0
    for i in range(len(years)):
        year_list.append(years[i])
        year_count_list.append(year_count[i])
        year_sum = year_sum + year_count[i]
    
    fuel = fuel_count.keys()
    fuel_list = []
    fuel_count_list = []
    fuel_sum = 0
    for i in range(len(fuel)):
        fuel_list.append(fuel[i])
        fuel_count_list.append(fuel_count[i])
        fuel_sum = fuel_sum + fuel_count[i]
    
    doors = door_count.keys()
    door_count = door_count.tolist()
    door_list = []
    door_count_list = []
    door_sum = 0
    for i in range(len(doors)):
        door_list.append(doors[i])
        door_count_list.append(door_count[i])
        door_sum = door_sum + door_count[i]
    
    seats = seat_count.keys()
    seat_count = seat_count.tolist()
    seat_list = []
    seat_count_list = []
    seat_sum = 0
    for i in range(len(seats)):
        seat_list.append(seats[i])
        seat_count_list.append(seat_count[i])
        seat_sum = seat_sum + seat_count[i]
    
    
    #print(year_list)
    #print(year_count_list)
    
    plt.figure(figsize=(30,5))
    plt.plot(maker_list,count_list/summ)
    plt.tight_layout()
    plt.show()
    
    #plt.figure(figsize=(10,5))
    #print(type(year_list))
    #print((year_count_list))
    for k in range(len(year_count_list)):
        year_count_list[k] = year_count_list[k]/year_sum
    plt.plot(year_list,year_count_list)
    plt.xticks(np.arange(min(year_list), max(year_list)+1, 5.0))
    plt.tight_layout()
    plt.show()
    
    plt.plot(fuel_list,fuel_count_list/fuel_sum)
    plt.tight_layout()
    plt.show()
    
    plt.xticks(np.arange(min(door_list), max(door_list)+1, 1.0))
    for k in range(len(door_count_list)):
        door_count_list[k] = door_count_list[k]/door_sum
    plt.plot(door_list,door_count_list)
    plt.tight_layout()
    plt.show()
        
    plt.plot(['auto','man'],[transmission_count[0]/1000,transmission_count[1]/1000])
    plt.tight_layout()
    plt.show()
    
    plt.xticks(np.arange(min(seat_list), max(seat_list)+1, 1.0))
    for k in range(len(seat_count_list)):
        seat_count_list[k] = seat_count_list[k]/seat_sum
    plt.plot(seat_list,seat_count_list)
    plt.tight_layout()
    plt.show()
    
if __name__ == '__main__':
    draw_PDF(preprocessing())
