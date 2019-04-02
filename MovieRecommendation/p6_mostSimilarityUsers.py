import pandas as pd
import p3_pearsonCC as pearson
import p4_commonRating as commonR
import p1_loadData as data
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import time
import PersonStandard as ps

#每个进程获取相似度函数
def getFunct(isAddD,isAddR,user,ratingsData,usersID):

    users_pearson_r = {"UserID":[],"degree":[],"commonMovieID":[]}  #先将数据保存到字典对象中
    commonRates = []
    for user2 in usersID:
        if user2 != user:
            commonData = commonR.getCommonRating(user,user2,ratingsData)
            if not commonData.empty :
                data1 = commonData["user"+str(user)].values
                data2 = commonData["user"+str(user2)].values

                if(data1.shape[0]>5):       #只有当共同评分的电影数量达到6个及以上的用户才能用于计算相似度，避免数据量太小导致的偶然性
                    commonMovieID = commonData["MovieID"].values

                    if isAddR:
                        commonRate = commonR.getCommonRate(user, user2, ratingsData)
                        commonRates.append(commonRate)

                    personVal = 1
                    if isAddD:
                        user2S = ps.getPersonStd(user2,ratingsData)
                        s_max = 1.8455128933988063
                        s_min = 0.12307692307692307

                        personVal = (user2S - s_min) / (s_max - s_min)
                    pearson_r = pearson.getPearsonCC(data1, data2, personVal)
                    #pearson_r = pearson.getPearsonCC(data1,data2)

                    users_pearson_r["degree"].append(pearson_r)
                    users_pearson_r["commonMovieID"].append(commonMovieID)
                    users_pearson_r["UserID"].append(user2)

    users_pearson_r = pd.DataFrame(users_pearson_r)     #转化位DataFrame格式
    return users_pearson_r,commonRates


#获取最相似的用户的接口函数
#传入目标用户，前n位最相似的用户，电影评分数据
#通过多进程降低程序运行时间
def getMostSimilarUsers(user,n,ratingsData,situation):

    usersData = data.getSourceData("usersData")     #读取用户数据
    usersID = usersData["UserID"].values  # 获取到所有用户ID
    futures = []    #保存每个进程得到的数据

    isAddD = False
    isAddR = False
    if situation == "rd" or situation == "rpd":
        isAddD = True
    if situation == "rp" or situation == "rpd":
        isAddR = True
    with ProcessPoolExecutor(max_workers=6) as p:       #定义四个进程，分别处理，降低程序执行时间
        # p=ThreadPoolExecutor(max_workers=4)

        future1 = p.submit(getFunct, isAddD,isAddR,user, ratingsData, usersID[:int(len(usersID)/6)])   #每个进程处理1/4的数据量
        future2 = p.submit(getFunct, isAddD,isAddR,user, ratingsData, usersID[int(len(usersID)/6):2*int(len(usersID)/6)])
        future3 = p.submit(getFunct, isAddD,isAddR,user, ratingsData, usersID[2*int(len(usersID)/6):3*int(len(usersID)/6)])
        future4 = p.submit(getFunct, isAddD,isAddR,user, ratingsData, usersID[3 * int(len(usersID) / 6):4 * int(len(usersID) / 6)])
        future5 = p.submit(getFunct, isAddD,isAddR,user, ratingsData, usersID[4 * int(len(usersID) / 6):5 * int(len(usersID) / 6)])
        future6 = p.submit(getFunct, isAddD,isAddR,user, ratingsData, usersID[5*int(len(usersID)/6):])
        futures.append(future1)     #将每个线程的结果保存进futures中
        futures.append(future2)
        futures.append(future3)
        futures.append(future4)
        futures.append(future5)
        futures.append(future6)

    #将每个进程的数据拼接在一个DataFrame中
    users_pearson_r = futures[0].result()[0]
    commonRates = np.array([])
    commonRates=np.append(commonRates,futures[0].result()[1])
    for future in futures[1:]:
        users_pearson_r = users_pearson_r.append(future.result()[0])
        commonRates = np.append(commonRates,future.result()[1])

    #排序数据，并获取前n位相似用户
    if isAddR:
        r_min = np.min(commonRates)
        r_max = np.max(commonRates)
        users_pearson_r["degree"]*=(commonRates-r_min) / (r_max-r_min)

    topN = users_pearson_r.sort_values(by="degree",ascending=False)[:n]
    topN.index = np.arange(0,n,1)
    return topN

# def readRatingsData():
#     ratingsData = data.getSourceData("ratingsData")  # 获取评分数据
#     return ratingsData

if __name__ == "__main__":
    user = int(input("Please input the user ID: "))  # 输入用户

    start = time.time()     #程序开始执行时间

    ratingsData = data.getSourceData("ratingsData")     #获取评分数据

    topFive = getMostSimilarUsers(user,5,ratingsData,"r")   #获取前5位相似度最高的用户

    print("The five most similar users are: ")
    print("-----------------------------------")
    print(topFive.drop("commonMovieID",1))

    print("-----------------------------------")
    print("Total time is: ",time.time()-start)