import pandas as pd
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import Perceptron, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier

# conts = ["arc153", "arc155", "arc156", "arc158"]
conts = ["arc141", "arc144", "arc149", "arc150", "arc153", "arc155", "arc156", "arc158"]
df = pd.read_csv('data_arc158.csv', usecols = conts)
df = df.fillna(0) # 欠損値を 0 埋め

drops = [] # 削除するリスト
for i in range(500):
    flag = 0 #欠損値の数
    for j in range(len(conts)):
        x = df.iat[i,j]
        y = 0
        if x == 0:
            flag += 1
        if x >= 15:
            y = 1
        df.iat[i,j] = y
    if flag >= 5: #欠損値が多いデータは考慮しない
        drops.append(i)

df = df.drop(df.index[drops])

df = df.sample(frac =1) #シャッフル

K = len(df)*3//5 # 訓練データの数
y_train = df["arc158"].values[:K]
y_test = df["arc158"].values[K:]
X_train = df.drop("arc158", axis=1).values[:K]
X_test = df.drop("arc158", axis=1).values[K:]

cnt = [0,0]
for i in range(len(X_test)):
    cnt[y_test[i]] += 1
print(cnt)

def perf_prediction(model, name):
    score = 0
    pred = model.predict(X_test)
    for i in range(len(X_test)):
        if pred[i] == y_test[i]:
            score += 1
    print(name,":",score/len(X_test))

model_svc = SVC().fit(X_train, y_train)
perf_prediction(model_svc, "SVC")

model_dtc = DecisionTreeClassifier().fit(X_train, y_train)
perf_prediction(model_dtc, "DecisionTreeClassifier")

model_Perceptron = Perceptron().fit(X_train, y_train)
perf_prediction(model_Perceptron, "Perceptron")

model_SGDC = SGDClassifier().fit(X_train, y_train)
perf_prediction(model_SGDC, "SGDC")

model_KN = KNeighborsClassifier().fit(X_train, y_train)
perf_prediction(model_KN, "KN")



model_VC = VotingClassifier(estimators=[('svc', model_svc), ('dt', model_dtc), ('kn', model_KN)]).fit(X_train, y_train)
perf_prediction(model_VC, "VC")

