import os
import numpy as np
import warnings
from getData import getdata,evaluate,MCC,Get_f1_score,Get_Accuracy,Get_Precision_score,Get_Recall
from xgboost import XGBClassifier
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
importence_rank =[]
ACC_list = []
flag_list =[]
PRE_list = []
REcall_list = []
F1_list = []
AUC_list =[]
MCC_list = []
sen_list = []
spe_list = []
def IFS(address):
    x_train,y_train,x_test,y_test = getdata(address)
    for i in range(len(importence_rank)):
        y_test = []
        y_train = []
        flag = importence_rank[i]
        fileList = os.listdir(address+"\\train\positive")
        flag_train = 0
        for name in fileList:
            x_train[flag_train].append(np.load(address+"\\train\positive\\" + name)[flag])
            y_train.append(1)
            flag_train+=1
        fileList = os.listdir(address+"\\train\\negitive")
        for name in fileList:
            x_train[flag_train].append(np.load(address+"\\train\\negitive\\" + name)[flag])
            y_train.append(0)
            flag_train += 1
        fileList = os.listdir(address+"\\test\positive")
        flag_test=0
        for name in fileList:
            x_test[flag_test].append(np.load(address+"\\test\positive\\" + name)[flag])
            y_test.append(1)
            flag_test += 1
        fileList = os.listdir(address+"\\test\\negitive")
        for name in fileList:
            x_test[flag_test].append(np.load(address+"\\test\\negitive\\" + name)[flag])
            flag_test += 1
            y_test.append(0)
        kf = KFold(n_splits=10)
        kf.get_n_splits(x_train)
        accuracy_ten = 0
        precision_ten = 0
        recall_ten = 0
        f1_score_ten = 0
        mcc_ten = 0
        auc_ten = 0
        sen_ten = 0
        spe_ten = 0
        x2_train, y2_train = shuffle(x_train, y_train, random_state=0)
        for train_index, test_index in kf.split(x_train):
            x1_train = []
            y1_train = []
            x1_test = []
            y1_test = []
            for i in range(len(train_index)):
                x1_train.append(x2_train[train_index[i]])
                y1_train.append(y2_train[train_index[i]])
            for i in range(len(test_index)):
                x1_test.append(x2_train[test_index[i]])
                y1_test.append(y2_train[test_index[i]])
            x1_train = np.array(x1_train)
            y1_train = np.array(y1_train)
            x1_test = np.array(x1_test)
            y1_test = np.array(y1_test)
            clf = XGBClassifier()
            clf.fit(x1_train, y1_train)
            y_predict = clf.predict(x1_test)
            score = clf.score(x1_test, y1_test)
            accuracy = Get_Accuracy(y1_test, y_predict)
            accuracy_ten += accuracy
            precision = Get_Precision_score(y1_test, y_predict)
            precision_ten += precision
            recall = Get_Recall(y1_test, y_predict)
            recall_ten += recall
            f1_score = Get_f1_score(y1_test, y_predict)
            f1_score_ten += f1_score
            mcc = MCC(y1_test, y_predict)
            mcc_ten += mcc
            sen,spe = evaluate(y1_test,y_predict)
            sen_ten +=sen
            spe_ten +=spe
        accuracy = accuracy_ten / 10
        precision = precision_ten / 10
        f1_score = f1_score_ten / 10
        mcc = mcc_ten / 10
        spe = spe_ten/10
        sen = sen_ten/10
        accuracy = round(accuracy,3)
        precision = round(precision,3)
        f1_score = round(f1_score,3)
        spe = round(spe,3)
        sen = round(sen,3)
        mcc = round(mcc,3)
        ACC_list.append(accuracy)
        PRE_list.append(precision)
        F1_list.append(f1_score)
        MCC_list.append(mcc)
        sen_list.append(sen)
        spe_list.append(spe)

