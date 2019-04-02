import p1_loadData as data
import p6_mostSimilarityUsers as msUsers
import pandas as pd
import numpy as np
import time
from collections import Counter
import matplotlib.pyplot as plt
import performance as pf

#用于求取推荐电影函数
#user为目标用户，n为相似用户数量（从前n个最相似的用户中获得推荐信息），m为获取的推荐电影数量
def getRecommendMovies(user,movieData,ratingsData,situation,n=4,m=10):

    n = 10   #取前n位最相似的用户用于推荐电影
    topN = msUsers.getMostSimilarUsers(user,n,ratingsData,situation)      #调用getFiveMostSimilarUsers接口获取具体相似度最高的前n位用户

    candidateMoviesSet = {"Rating":[],"MovieID":[]}     #通过这n位相似用户观看过的电影推荐给此用户
    for i in topN.index:
        simi_user = topN.loc[i]["UserID"]
        commonMovie = topN.loc[i]["commonMovieID"]  #获取到当前用户和当前相似用户所观看过的相同电影
        simi_user_data = ratingsData[ratingsData['UserID'] == simi_user]  # 获取用户i的评级数据

        for movie in commonMovie:   #从推荐用户所观看过的电影中删除当前用户已经观看过的电影（不能向用户推荐其已经观看过的电影）
            simi_user_data = simi_user_data.drop(simi_user_data[simi_user_data["MovieID"]==movie].index)

        simi_user_data["Rating"]*=topN.loc[i]["degree"]     #将每个推荐用户对当前用户没有观看过的电影所打的评级乘上两个用户的相似度，最后用于所有电影项用户推荐顺序的依据

        #recommendMoviesDataSet用于收集待推荐电影数据
        candidateMoviesSet["Rating"] = np.append(candidateMoviesSet["Rating"],simi_user_data["Rating"].values)
        candidateMoviesSet["MovieID"] = np.append(candidateMoviesSet["MovieID"],simi_user_data["MovieID"].values)

    candidateMoviesSet = pd.DataFrame(candidateMoviesSet)

    m = 10  #只取排名前m的电影推荐给用户
    candidateMoviesSet = candidateMoviesSet.sort_values(by="Rating",ascending=False)[:m]

    #recommendMoviesSet用于保存最终确定的要推荐的电影的所有信息
    recommendMoviesSet = movieData[movieData["MovieID"]==candidateMoviesSet["MovieID"].values[0]]
    for movieID in candidateMoviesSet["MovieID"].values[1:]:    #从电影数据中得到相应MovieID的所有信息
        set = movieData[movieData["MovieID"]==movieID]
        recommendMoviesSet = recommendMoviesSet.append(set)

    recommendMoviesSet.index = np.arange(0,m,1)
    return recommendMoviesSet,candidateMoviesSet["Rating"].values

#接口测试
if __name__ == "__main__":
    #user = int(input("Please input the user ID: "))  # 输入用户

    movieData = data.getSourceData("movieData")  # 获取电影数据
    ratingsData = data.getSourceData("ratingsData")  # 获取电影评级数据

    start = time.time()

    T_WC = []
    T_CC = []
    T_Cover = []
    count = 0
    uus = np.arange(50,151,1)#np.random.randint(1, 6040, size=100)
    for situation in ["r","rp","rd","rpd"]:
        WC = []
        CC = []
        Cover = []

        for u in uus:#range(100,201):
            recommondMovies,rating = getRecommendMovies(u,movieData,ratingsData,situation)

            user_rd = ratingsData[ratingsData["UserID"] == u]

            user_rd = user_rd[user_rd["Rating"] > 3]

            user_rd.index = np.arange(0, user_rd.shape[0])

            movies = pd.DataFrame({"MovieID": [], "Title": [], "Genres": []})
            for m in user_rd["MovieID"].values:
                mo = movieData[movieData["MovieID"] == m]
                movies = movies.append(mo)

            movies.index = np.arange(0, movies.shape[0])
            ori_x = []
            ori_y = []
            for i in range(user_rd.shape[0]):
                for g in movies["Genres"][i].split("|"):
                    if not g in ori_x:
                        ori_x.append(g)
                        ori_y.append(user_rd["Rating"][i])
                    else:
                        index = ori_x.index(g)
                        ori_y[index] += user_rd["Rating"][i]

            res_x = []
            res_y = []
            for i in range(recommondMovies.shape[0]):
                for g in recommondMovies["Genres"][i].split("|"):
                    if not g in res_x:
                        res_x.append(g)
                        res_y.append(rating[i])
                    else:
                        index = res_x.index(g)
                        res_y[index] += rating[i]

            res_y = list(np.array(res_y) / np.max(res_y))

            wc, cover, cc = pf.getPerformance(res_x,res_y,ori_x,ori_y)

            WC.append(wc)
            CC.append(cc)
            Cover.append(cover)
            print(u)

        print("--------",count,"---------")
        count+=1

        T_WC.append(WC)
        T_CC.append(CC)
        T_Cover.append(Cover)

    print("WC:",np.mean(T_WC,axis=1))
    print("CC:",np.mean(T_CC,axis=1))
    print("Cover:",np.mean(T_Cover,axis=1))
        # plt.bar(genres, score,color="w",edgecolor="k",hatch="/////")
        # plt.xlabel("电影类别", fontsize=19)
        # plt.ylabel("总得分", fontsize=19)
        # plt.tick_params(labelsize=12.5)
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        # plt.show()