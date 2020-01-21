import os
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn import metrics
def evaluate(y_true,y_pred):
    TN,FP,FN,TP =confusion_matrix(y_true,y_pred,labels=[0,1]).ravel()
    spe = round(TN/(TN+FP),3)
    sen = round(TP/(TP+FN),3)
    print("sen =", sen)
    print("spe =",spe)

def MCC(y_ture,y_pred):
    mcc = metrics.matthews_corrcoef(y_ture,y_pred)
    return mcc
def Get_Accuracy(y_true, y_pred):  # Accuracy 准确率：分类器正确分类的样本数与总样本数之比
    accuracy = metrics.accuracy_score(y_true, y_pred)
    return accuracy

def Get_Precision_score(y_true, y_pred):  # Precision：精准率 正确被预测的正样本(TP)占所有被预测为正样本(TP+FP)的比例.
    precision = metrics.precision_score(y_true, y_pred)
    return precision

def Get_Recall(y_true, y_pred):  # Recall 召回率 正确被预测的正样本(TP)占所有真正 正样本(TP+FN)的比例.
    Recall = metrics.recall_score(y_true, y_pred)
    return Recall


def Get_f1_score(y_true, y_pred):  # F1-score: 精确率(precision)和召回率(Recall)的调和平均数
    f1_score = metrics.f1_score(y_true, y_pred)
    return f1_score


def Get_Auc_value(y_true, y_proba):
    # fpr, tpr, thresholds = metrics.roc_curve(samples_test_y, proba_pred_y, pos_label=2)
    auc = metrics.roc_auc_score(y_true, y_proba)
    return auc
def getdata(address):
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    fileList = os.listdir(address+"\\train\positive")
    flag = 0
    for name in fileList:
        flag += 1
        x_train.append(np.load(address+"\\train\positive\\" + name))
        # print(np.load("D:\PycharmWorkspace\zyh\Data\\train\positive\\"+name))
        y_train.append(1)
    fileList = os.listdir(address+"\\train\\negitive")
    flag = 0
    for name in fileList:
        flag += 1
        x_train.append(np.load(address+"\\train\\negitive\\" + name))
        y_train.append(0)
    fileList = os.listdir(address+"\\test\positive")
    flag = 0
    for name in fileList:
        flag += 1
        x_test.append(np.load(address+"\\test\positive\\" + name))
        y_test.append(1)
    fileList = os.listdir(address+"\\test\\negitive")
    flag = 0
    for name in fileList:
        flag += 1
        x_test.append(np.load(address+"\\test\\negitive\\" + name))
        y_test.append(0)
    return x_train,y_train,x_test,y_test