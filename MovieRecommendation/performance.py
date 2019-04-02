import numpy as np

def getPerformance(res_x,res_y,ori_x,ori_y):

    wc = 0
    for i in range(len(res_x)):
        r = 0
        if res_x[i] in ori_x:
            index = ori_x.index(res_x[i])
            r = res_y[i] * (ori_y[index]+1)/(sum(ori_y)+17)
        else:
            r = res_y[i] * 1/(sum(ori_y)+17)
        wc += r

    common = np.intersect1d(res_x,ori_x)
    total = np.unique(np.append(res_x,ori_x))
    cover = len(common)/len(total)
    cc = wc*cover
    return wc,cover,cc

if __name__ == "__main__":
    # 改进前r
    # res_x = ['Action', 'Drama', 'War', "Children's", 'Comedy', 'Romance']
    # res_y = [0.1, 1,  0.1, 0.1, 0.3, 0.2]

    # 加入r+p
    # res_x = ['Comedy', 'War', 'Animation', "Children's", 'Adventure', 'Fantasy', 'Sci-Fi', 'Drama', 'Thriller', 'Action', 'Horror', 'Musical', 'Romance']
    # res_y = [1,0.16666667, 0.16666667, 0.33333333, 0.33333333, 0.16666667,0.33333333, 0.16666667, 0.33333333, 0.16666667, 0.33333333, 0.16666667,0.33333333]

    # 加入r+d
    res_x = ['Drama', 'War', 'Action', 'Adventure', 'Comedy', 'Crime', 'Thriller', 'Documentary', 'Musical']
    res_y = [1, 0.25, 0.375, 0.125, 0.25, 0.25, 0.125, 0.125, 0.125]

    # 加入r+p+d
    # res_x = ['Adventure', "Children's", 'Comedy', 'Fantasy', 'Sci-Fi', 'Musical', 'Romance', 'Animation', 'Drama', 'Action', 'Thriller', 'Horror']
    # res_y = [0.75, 0.75, 1, 0.25, 0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5,  0.5 ]

    ori_x = ['Drama', 'Animation', "Children's", 'Comedy', 'Action', 'Adventure', 'Musical', 'Fantasy', 'Sci-Fi', 'War',
             'Romance', 'Thriller', 'Crime']
    ori_y = [93, 62, 79, 49, 18, 17, 54, 12, 13, 10, 13, 8, 8]

    print(getPerformance(res_x,res_y,ori_x,ori_y))