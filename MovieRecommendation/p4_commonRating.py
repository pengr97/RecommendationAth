import pandas as pd
import p1_loadData as data
import numpy as np
import time
from concurrent.futures import ProcessPoolExecutor

def getCommonRating(user1,user2,ratingsData):

    user1_data = ratingsData[ratingsData['UserID']==user1]      #获取用户1的评级数据
    user2_data = ratingsData[ratingsData['UserID']==user2]      #获取用户2的评级数据

    result = {"MovieID":[],"user"+str(user1):[],"user"+str(user2):[]}       #此字典用于保存两个用户对相同电影的评分数据，最后保存为DataFrame对象，格式化输出
    for movieID in user1_data["MovieID"].values:    #遍历循环两个用户相同的电影数据
        if movieID in user2_data["MovieID"].values:
            result["MovieID"].append( movieID)
            result["user"+str(user1)].append(user1_data[user1_data["MovieID"]==movieID]["Rating"].values[0])
            result["user"+str(user2)].append(user2_data[user2_data["MovieID"]==movieID]["Rating"].values[0])

    result = pd.DataFrame(result)   #转化为DataFrame对象
    return result

#通过多进程降低程序运行时间
def getCommonRate(user1,user2,ratingsData):

    user1_data = ratingsData[ratingsData['UserID'] == user1]["MovieID"].values  # 获取用户1的评级电影
    user2_data = ratingsData[ratingsData['UserID'] == user2]["MovieID"].values  # 获取用户2的评级电影
    commonMovies = np.intersect1d(user1_data, user2_data)
    totalMovies = np.unique(np.append(user1_data, user2_data))
    commonRate = commonMovies.shape[0] / totalMovies.shape[0]


    return commonRate

#模块测试
if __name__ =="__main__":

    user1 = int(input("Please input the first user ID: "))  # 输入用户1
    user2 = int(input("Please input the second user ID: "))  # 输入用户2

    usersData = data.getSourceData("usersData")  # 读取用户数据
    usersID = usersData["UserID"].values  # 获取到所有用户ID

    start = time.time()  # 程序开始执行时间
    ratingsData = data.getSourceData("ratingsData")  # 获取评分数据
    #result = getCommonRating(user1,user2,ratingsData)   #调用函数
    commonMovies = getCommonRate(user1,user2,ratingsData,usersID)
    print("The same movies's ratings of user"+str(user1)+" and user"+str(user2)+" is：")
    print("-----------------------------------")
    # if(result.empty):
    #     print("There are no common rating between these two users!")
    # else:
    #     print(result)
    print("-----------------------------------")
    print("Total merge movies:",commonMovies)
    print("Total time is: ", time.time() - start)