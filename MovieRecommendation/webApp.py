from flask import Flask
from flask import render_template
from flask import request
import p1_loadData as data
import p4_commonRating as commonR
import p5_similarityDegree as simiDeg
import p6_mostSimilarityUsers as simiUsers
import p7_recommendMovies as recMovies
import pandas as pd

app = Flask(__name__)


#公共数据，保存原始数据
ratingsData = pd.DataFrame()
movieData = pd.DataFrame()
usersData = pd.DataFrame()

#web根目录
@app.route('/')
def index():
    return render_template("index.html",Data = {"index":-1,"movieData":"","usersData":"","ratingsData":""})

#获取源数据路由
@app.route('/getData',methods = ['POST'])
def getData():

    global ratingsData,movieData,usersData
    if movieData.empty:
        movieData = data.getSourceData("movieData")
    if usersData.empty:
        usersData = data.getSourceData("usersData")
    if ratingsData.empty:
        ratingsData = data.getSourceData("ratingsData")
    sourceData = {"movieData":movieData,"usersData":usersData,"ratingsData":ratingsData}

    return render_template("Q1.resourceData.html",Data = sourceData)

#获取输入面板
@app.route('/getInputPage',methods = ['POST'])
def getInputPage():
    index = int(request.form.get("index", 2))

    if index==1:
        return render_template("Q3.answer.html")
    elif index==2:
        return render_template("Q4.commonR.html")
    elif index==3:
        return render_template("Q5.simiDeg.html")
    elif index==4:
        return render_template("Q6.fiveUsers.html")
    else:
        return render_template("Q7.recMovies.html")

#第四问路由接口
@app.route('/getQ4Ans',methods = ['POST'])
def getQ4Ans():
    global ratingsData
    users = request.form.get("val","0 1")
    users = [int(u) for u in users.split(" ")]
    if ratingsData.empty:
        ratingsData = data.getSourceData("ratingsData")

    commR = commonR.getCommonRating(users[0],users[1],ratingsData)
    return render_template("Q4.answer.html",commR=commR)

#第五问路由接口
@app.route('/getQ5Ans',methods = ['POST'])
def getQ5Ans():
    global ratingsData
    users = request.form.get("val", "0 1")
    users = [int(u) for u in users.split(" ")]
    if ratingsData.empty:
        ratingsData = data.getSourceData("ratingsData")

    simiD = simiDeg.getSimiDeg(users[0],users[1],ratingsData)

    return render_template("Q5.answer.html", simiD=simiD)

#第六问路由接口
@app.route('/getQ6Ans',methods = ['POST'])
def getQ6Ans():
    global ratingsData
    user = request.form.get("val", "0")
    user = int(user)
    if ratingsData.empty:
        ratingsData = data.getSourceData("ratingsData")

    fiveUsers = simiUsers.getMostSimilarUsers(user,5,ratingsData)

    return render_template("Q6.answer.html", fiveUsers=fiveUsers)

#第七问路由接口
@app.route('/getQ7Ans',methods = ['POST'])
def getQ7Ans():
    global ratingsData
    user = request.form.get("val", "0")
    user = int(user)
    if ratingsData.empty:
        ratingsData = data.getSourceData("ratingsData")

    movies = recMovies.getRecommendMovies(user)

    return render_template("Q7.answer.html", movies=movies)


if __name__ == '__main__':
    app.run(debug=True)
