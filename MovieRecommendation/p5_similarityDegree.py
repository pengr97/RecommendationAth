import p4_commonRating as commonR
import p3_pearsonCC as pearson
import p1_loadData as data
import PersonStandard as ps

def getSimiDeg(user1,user2,ratingsData,usersID):

    commonData = commonR.getCommonRating(user1,user2,ratingsData)     #调用commonRating模块中的getCommonRating函数，获取两个用户对相同电影的评级

    if commonData.empty:
        print("There are no common rating between these two users!")
        exit(0)
    data1 = commonData["user"+str(user1)].values    #分别获取到两用户的评级数据，转化为numpy格式
    data2 = commonData["user"+str(user2)].values

    commonRate = commonR.getCommonRate(user1,user2,ratingsData)
    user2S = ps.getPersonStd(user2)
    s_max = 1.8455128933988063
    s_min = 0.12307692307692307
    personVal = (user2S-s_min) / (s_max-s_min)

    pearson_r = pearson.getPearsonCC(data1,data2,personVal,commonRate)  #调用pearson相关系数模块的personCC函数求解两用户的相似度

    return pearson_r

if __name__ =="__main__":
    user1 = int(input("Please input the first user ID: "))  # 输入用户1
    user2 = int(input("Please input the second user ID: "))  # 输入用户2
    ratingsData = data.getSourceData("ratingsData")

    usersData = data.getSourceData("usersData")  # 读取用户数据
    usersID = usersData["UserID"].values  # 获取到所有用户ID

    for u in usersID[1:]:
        pearson_r = getSimiDeg(user1, u, ratingsData,usersID)
        print(pearson_r)

    print("-----------------------------------")
    print("The similarity degree between user"+str(user1)+" and user"+str(user2)+" is:",pearson_r)
    print("-----------------------------------")
