import pandas as pd
import numpy as np
import time
from collections import Counter
import matplotlib.pyplot as plt

def getSourceData(data):
    #通过pandas的read_table函数读取文件数据
    sourceData = ""
    if data=="movieData":
        sourceData = pd.read_table("SourceData/movies.dat",sep="::",names=["MovieID","Title","Genres"])
    elif data=="usersData":
        sourceData = pd.read_table("SourceData/users.dat",sep="::",names=["UserID","Gender","Age","Occupation","Zip-code"])
    elif data=="ratingsData":
        #sourceData = pd.read_table("SourceData/ratings.dat",sep="::",names=["UserID","MovieID","Rating","Timestamp"])  #read_table函数读取数据较慢需要10秒左右，改用open后只需2秒
        sourceData= {  # 以字典对象保存每个人的信息
            'UserID': [],  # 将读取的数据按逗号分割
            'MovieID': [],
            'Rating': [],
            'Timestamp': []
        }
        for line in open("SourceData/ratings.dat"):  # 按行读取数据
            line = line.strip("\n")  # 删除数据中的换行符
            line = line.split('::')
            sourceData["UserID"].append(int(line[0]))
            sourceData["MovieID"].append(int(line[1]))
            sourceData["Rating"].append(int(line[2]))
            sourceData["Timestamp"].append(int(line[3]))

        sourceData = pd.DataFrame(sourceData)
    return sourceData

if __name__ == "__main__":
    # start = time.time()
    # print("电影数据：\n",getSourceData("movieData"))
    # print("用户数据：\n",getSourceData("usersData"))
    # print("评级数据：\n",getSourceData("ratingsData"))
    # print("Total time: ",time.time()-start)

    movieData = getSourceData("movieData")
    ratingsData = getSourceData("ratingsData")

    user1_rd = ratingsData[ratingsData["UserID"]==1]
    print(user1_rd.shape)
    user1_rd = user1_rd[user1_rd["Rating"]>3]
    print(user1_rd.shape)
    user1_rd.index = np.arange(0, user1_rd.shape[0])

    movies = pd.DataFrame({"MovieID":[],"Title":[],"Genres":[]})
    for m in user1_rd["MovieID"].values:
        mo = movieData[movieData["MovieID"]==m]
        movies = movies.append(mo)

    movies.index = np.arange(0,movies.shape[0])
    #print(movies)

    genres = []
    score = []
    for i in range(user1_rd.shape[0]):
        for g in movies["Genres"][i].split("|"):
            if not g in genres:
                genres.append(g)
                score.append(user1_rd["Rating"][i])
            else:
                index = genres.index(g)
                score[index] += user1_rd["Rating"][i]

    print(genres)
    print(score)

    plt.bar(genres,score,color="w",edgecolor="k",hatch="/////")
    plt.xlabel("电影类别",fontsize=19)
    plt.ylabel("总评分",fontsize=19)
    plt.tick_params(labelsize=12.5)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.show()