from sklearn.ensemble import ExtraTreesClassifier
from getData import getdata,evaluate,MCC,Get_f1_score,Get_Accuracy,Get_Precision_score,Get_Recall
clf = ExtraTreesClassifier()
address = ''
x_train,y_train,x_test,y_test = getdata(address)
clf.fit(x_train, y_train)
y_predict = clf.predict(x_test)
accuracy = Get_Accuracy(y_test,y_predict)
accuracy = round(accuracy,3)
precision = Get_Precision_score(y_test ,y_predict)
precision = round(precision,3)
recall = Get_Recall(y_test,y_predict)
recall = round(recall,3)
f1_score = Get_f1_score(y_test,y_predict)
f1_score = round(f1_score,3)
mcc = MCC(y_test,y_predict)
mcc = round(mcc,3)
print('\n')
evaluate(y_test,y_predict)
print("Precision = ",precision)
print("Accuracy_Score = ",accuracy)
print("F1-Score  = ",f1_score)
print("MCC = ",mcc)

