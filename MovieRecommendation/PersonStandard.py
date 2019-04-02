import pandas as pd
import p1_loadData as data
import numpy as np
import time

s_max = 1.8455128933988063
s_min = 0.12307692307692307

# 求最小和最大的标准差
def getS_MinMax(ratingsData,users):

    u_ratingData = ratingsData[ratingsData["UserID"]==users[0]]["Rating"].values
    u_s = np.std(u_ratingData)
    s_min = u_s
    s_max = u_s
    for u in users[1:]:
        u_ratingData = ratingsData[ratingsData["UserID"]==u]["Rating"].values
        u_s = np.std(u_ratingData)
        if(u_s>s_max):
            s_max = u_s
        elif(u_s<s_min):
            s_min = u_s
    return s_min,s_max

def getPersonStd(user,ratingsData):

    return np.std(ratingsData[ratingsData["UserID"]==user]["Rating"].values)

if __name__ == "__main__":
    ratingsData = data.getSourceData("ratingsData")
    # usersData = data.getSourceData("usersData")
    # users = usersData["UserID"].values
    # s_min, s_max = getS_MinMax(ratingsData,users)
    # print("s_min:", s_min)
    # print("s_max:", s_max)

    p_val = getPersonStd(1,ratingsData)
    print("person val:",p_val)