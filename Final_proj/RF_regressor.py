import pandas as pd
from sklearn import svm
df = pd.read_csv('train.csv')
#df = df.sample(frac=0.1)
dflist = df.values.tolist()

tdf = pd.read_csv('test.csv')
#tdf = tdf.sample(frac=0.1)
tdflist = tdf.values.tolist()


training_predict = []
for i in range(len(dflist)):
    training_predict.append(dflist[i][-1])
    dflist[i] = dflist[i][:-1]
    
testing_predict = []
for i in range(len(tdflist)):
    testing_predict.append(tdflist[i][-1])
    tdflist[i] = tdflist[i][:-1]

maker_list = []
for i in range(len(dflist)):
    maker_list.append(dflist[i][0])
ml = list(set(maker_list))
ml.sort()

tmaker_list = []
for i in range(len(tdflist)):
    tmaker_list.append(tdflist[i][0])
tml = list(set(tmaker_list))
tml.sort()

model_list = []
for i in range(len(dflist)):
    model_list.append(dflist[i][1])
md = list(set(model_list))
md.sort()

tmodel_list = []
for i in range(len(tdflist)):
    tmodel_list.append(tdflist[i][1])
tmd = list(set(tmodel_list))
tmd.sort()

gas_list = []
for i in range(len(dflist)):
    gas_list.append(dflist[i][9])
gas = list(set(gas_list))
gas.sort()

tgas_list = []
for i in range(len(tdflist)):
    tgas_list.append(tdflist[i][9])
tgas = list(set(tgas_list))
tgas.sort()

for i in range(len(dflist)):
    for k in range(len(ml)):
        if dflist[i][0] == ml[k]:
            dflist[i][0] = k

for i in range(len(tdflist)):
    for k in range(len(tml)):
        if tdflist[i][0] == tml[k]:
            tdflist[i][0] = k

for i in range(len(dflist)):
    for k in range(len(md)):
        if dflist[i][1] == md[k]:
            dflist[i][1] = k

for i in range(len(tdflist)):
    for k in range(len(tmd)):
        if tdflist[i][1] == tmd[k]:
            tdflist[i][1] = k
            
for i in range(len(dflist)):
    if dflist[i][6] == 'man':
        dflist[i][6] = 0
    elif dflist[i][6] =='auto':
        dflist[i][6] = 1
        
for i in range(len(tdflist)):
    if tdflist[i][6] == 'man':
        tdflist[i][6] = 0
    elif tdflist[i][6] =='auto':
        tdflist[i][6] = 1        

for i in range(len(dflist)):
    for k in range(len(gas)):
        if dflist[i][9] == gas[k]:
            dflist[i][9] = k

for i in range(len(tdflist)):
    for k in range(len(tgas)):
        if tdflist[i][9] == tgas[k]:
            tdflist[i][9] = k
            
#dflist

#clf = svm.SVR()
#svm = clf.fit(dflist,training_predict)
#ans = svm.predict(tdflist)

#for i in range(len(ans)):
    #print(ans[i])

#dflist

from sklearn.ensemble import RandomForestRegressor
regr = RandomForestRegressor(random_state=0)
regr.fit(dflist, training_predict)
ans = regr.predict(tdflist)
ans


count = 0
for i in range(len(ans)):
    error = ans[i]-testing_predict[i]
    if abs(error) <1000:
        count = count + 1
print(count/len(ans))
