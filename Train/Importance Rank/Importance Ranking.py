from sklearn.ensemble import RandomForestClassifier
from getData import getdata,evaluate,MCC,Get_f1_score,Get_Accuracy,Get_Precision_score,Get_Recall
clf = RandomForestClassifier()
address = ''
x_train,y_train,x_test,y_test = getdata(address)
clf.fit(x_train, y_train)
importence = clf.feature_importances_
print(importence)