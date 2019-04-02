import numpy as np

def getPearsonCC(data1,data2,personVal=1,comonRate=1):
    data1_ave = np.mean(data1)  #数据1的平均值
    data2_ave = np.mean(data2)  #数据2的平均值
    numerator = np.sum((data1-data1_ave)*(data2-data2_ave))     #pearson相关系数的分子
    denominator = np.sqrt(np.sum((data1-data1_ave)*(data1-data1_ave)))*np.sqrt(np.sum((data2-data2_ave)*(data2-data2_ave)))     #pearson相关系数的分母

    if(denominator==0):
        return 0

    pearson_r = numerator/(denominator)*personVal*comonRate   #pearson相关系数
    return pearson_r