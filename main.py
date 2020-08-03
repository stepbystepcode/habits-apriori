# -*- coding: UTF-8 -*-
import pandas as pd
import itertools
#读取数据并进行编号和转换
def prepare():
    data = pd.read_csv('data.csv', header=None)
    data = data.iloc[1:,12:21]
    data.columns = ["1","2","3","4","5","6","7","8","9"]
    return data
def change_mean(data):
    habits = ["有计划","预习","记笔记","主动回答问题","有问题及时提问","复习","认真完成作业","及时订正错题","成绩好"]
    out = []
    for i in range(len(data.values)):
        for j in range(len(habits)):
            if data.values[i][j]=="1":
                data.values[i][j]=habits[j]
    out = data.values.tolist()
    for row in out:
        for i in range(len(row)-1,-1,-1):
            if row[i] == "2":
                row.remove(row[i])
    return out
datas = change_mean(prepare())
def load_dataSet(data):
    # , error_bad_lines = False, index_col=0
    #利用pandas读取数据
    # print('----')
    goods = []
    goodsList = {}
    change_data= []
    #print(data)
    #对商品进行编号
    for key in data:
        #key = key[0]
        #key = key.split(',')
        for i in key:
            if i not in goods:
                goods.append(i)

    for key in range(len(goods)):
        goodsList[goods[key]] = key + 1

    #输出习惯的编号
    print('习惯编号：', goodsList)

    #转换数据
    for key in data:
        key_num = []
        #key = key[0].split(',')

        for i in key:
            key_num.append(goodsList[i])

        key_num.sort()
        change_data.append(key_num)

    #输出转换后的数据
    #print('\n转换后的数据：', change_data)

    return goodsList, change_data

#Apriori算法，其中s是最小支持度,data是数据集,data_iter是迭代中的数据集,c是输出的频繁项集,s是频繁项集对应的支持度
def apriori(s_min, data, data_iter, s=[], c=[], i=1):
    if len(data_iter) != 0:
        goods = separate(data_iter, i)
        data_iter = []
        for good in goods:
            num = 0
            for key in data:
                if set(good) <= set(key):
                    num = num + 1
            if num >= s_min:
                c.append(good)
                s.append(num)
                data_iter.append(good)

        apriori(s_min, data, data_iter, s, c, i=i+1)

#separate函数用于将data中的数据进行排列组合，i是组合的大小
def separate(data, i):
    a = []
    b = []
    for k in data:
        for j in range(len(k)):
            if k[j] not in a:
                a.append(k[j])

    if i <= len(a):
        for k in itertools.combinations(a, i):
            b.append(list(k))
    return b

#根据频繁项集获取关联规则，c是最小置信度，S是置信度列表，C是频繁项集
def get_associationRules(c, S, C, goodList):
    for key in C:
        a = []
        b = []
        if len(key) > 1:
            for i in key:
                a.append([i])
                b.append(list(goodList.keys())[list(goodList.values()).index(i)])

            for a_value in a:
                a_value_c = S[C.index(a_value)]
                key_c = S[C.index(key)]
                if key_c/a_value_c >= c:
                    # print(a_value, ' ---> ', key, ' : ', key_c/a_value_c)
                    value = list(goodList.keys())[list(goodList.values()).index(a_value[0])]
                    d = b.copy()
                    d.remove(value)
                    if d == ["成绩好"]:
                        print([list(goodList.keys())[list(goodList.values()).index(a_value[0])]],
                              ' ---> ', d, ' : ', key_c/a_value_c)

if __name__ == '__main__':
    goodList, data = load_dataSet(datas)

    C = []
    C1 = []
    S = []
    #设置最小支持度为4
    apriori(4, data, data, S, C)

    for value in C:
        a = []
        for i in value:
            a.append(list(goodList.keys())[list(goodList.values()).index(i)])
        C1.append(a)

   # print('支持度：', S)
   # print('频繁项集：', C)
   # print(C1)

    print('\n频繁项集的支持度')
    for i in range(len(C1)):
        if len(C1[i]) == 1:
            print(C1[i], '的支持度:', S[i])

    #输出关联规则
    print('\n关联规则:置信度')
    get_associationRules(0.6, S, C, goodList)
