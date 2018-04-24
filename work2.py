# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 21:59:56 2018

@author: Libo
"""

import pandas as pd
import numpy as np

#对数据集进行处理，转换成适合关联规则挖掘的形式；
def loadDataSet():
    
    df = pd.read_csv('Building_Permits.csv', low_memory=False)
    rule = ['Permit Type','Street Number','Current Status','Estimated Cost', 'Proposed Units', 'Existing Construction Type']
# 格式化属性名称
    rule_label = []
    for column in rule:
        column =  column.replace(' ','_')
        rule_label.append(column)
    print(rule_label)    
    data = df[rule]
    trans_dict = {}
    record_num = data.index.__len__()
    for column in rule:
        new_line = [""]*record_num
        for index in data.index:
            item = data[column][index]
            try:
                if np.isnan(item):
                    new_line[index] = ""
                else:
# 拼接属性和属性值,输出新的数据集:
                    new_line[index] = rule_label[rule.index(column)] + "_"+ str(item).replace(' ','_')
            except BaseException as e:
                new_line[index] = rule_label[rule.index(column)] + "_" + str(item).replace(' ','_')
        trans_dict[column] = new_line
    data_csv = pd.DataFrame(trans_dict)
    data_csv.to_csv('Ar_data.csv', index=False, header=False)
    
    data_set = [line.split() for line in open("Ar_data.csv").readlines()]
#    data_set = []
#    file_iter = open(data_csv, mode = "r+", newline = "")
#    for line in file_iter:
#        line = line.strip().rstrip(',')
#        s = line.split(',')
#        while '' in s:
#            s.remove('')
#        data_set.append(s)
#    print(len(data_set))
    return data_set
# 创建集合 C1。即对 dataSet 进行去重，排序，放入 list 中，然后转换所有的元素为 frozenset
def createC1(dataset):
    """
    createC1（创建集合 C1）
    Args:
        dataSet 原始数据集
    Returns:
        frozenset 返回一个 frozenset 格式的 list

    """

    C1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in C1:
                # 遍历所有的元素，如果不在 C1 出现过，那么就 append
                C1.append([item])#使用列表作为C1元素是因为后续需要使用集合操作
    # 对数组进行 `从小到大` 的排序
    # print 'sort 前=', C1
    C1.sort()
    # frozenset 表示冻结的 set 集合，元素无改变；可以把它当字典的 key 来使用
    # print 'sort 后=', C1
    # print 'frozenset=', map(frozenset, C1)
#    print(len(C1))
    return map(frozenset, C1)

def scanDataSet(dataset,Ck,minSupport):
    '''
    输入：DataSet应为每条记录是set类型数据（被用于判断是否是其子集操作），Ck中的每个项集为frozenset型数据（被用于字典关键字）
         Ck为候选频繁项集，minSupport为判断是否为频繁项集的最小支持度（认为给定）
    功能：从候选项集中找出支持度support大于最小支持度minSupport的频繁项集
    输出：频繁项集集合returnList,以及频繁项集对应的支持度support
    '''
    subSetCount = {}#临时存放选数据集 Ck 的频率
    for transction in dataset:#取出数据集dataset中的每行记录
        for subset in Ck:#取出候选频繁项集Ck中的每个项集
            if subset.issubset(transction):#判断Ck中项集是否是数据集每条记录数据集合中的子集
                if subset not in subSetCount:
                    subSetCount[subset] = 1
                else:
                    subSetCount[subset] += 1
    numItem = float(len(dataset))
    print(numItem)
    returnList =[]
    returnSupportData = {}
    for key in subSetCount:
        support = subSetCount[key]/numItem # 支持度 = 候选项（key）出现的次数 / 所有数据集的数量
        if support >= minSupport:
            returnList.insert(0,key)  # 在 retList 的首位插入元素，只存储支持度满足频繁项集的值
            returnSupportData[key] = support # 存储所有的候选项（key）和对应的支持度（support）
    return returnList,returnSupportData

def createCk(Lk,k):
    """
    输入频繁项集列表 Lk 与返回的元素个数 k，然后输出候选项集 Ck。
    Args:
        Lk 频繁项集列表
        k 返回的项集元素个数（若元素的前 k-2 相同，就进行合并）
    Returns:
        returnList 元素两两合并的数据集
    """
    returnList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k-2];L2 = list(Lk[j])[:k-2]
            L1.sort();L2.sort()
            if L1 == L2:#只需取前k-2个元素相等的候选频繁项集即可组成元素个数为k+1的候选频繁项集！！
                returnList.append(Lk[i] | Lk[j])    
    return returnList

# 找出数据集 dataSet 中支持度 >= 最小支持度的候选项集以及它们的支持度。即我们的频繁项集。
def apriori(dataset, minSupport=0.5):

    """
    apriori（首先构建集合 C1，然后扫描数据集来判断这些只有一个元素的项集是否满足最小支持度的要求。那么满足最小支持度要求的项集构成集合 L1。然后 L1 中的元素相互组合成 C2，C2 再进一步过滤变成 L2，然后以此类推，知道 CN 的长度为 0 时结束，即可找出所有频繁项集的支持度。）
    Args:
        dataSet 原始数据集
        minSupport 支持度的阈值
    Returns:
       L 频繁项集的全集
        supportData 所有元素和支持度的全集
    """
    # C1 即对 dataSet 进行去重，排序，放入 list 中，然后转换所有的元素为 frozenset
    C1 = createC1(dataset)
    # print 'C1: ', C1
    # 对每一行进行 set 转换，然后存放到集合中
    D = list(map(set, dataset))

    # 计算候选数据集 C1 在数据集 D 中的支持度，并返回支持度大于 minSupport 的数据
    L1, supportData = scanDataSet(D, C1, minSupport)
    # print "L1=", L1, "\n", "outcome: ", supportData

    # L 加了一层 list, L 一共 2 层 list
    L = [L1]
    k = 2
    # 判断 L 的第 k-2 项的数据长度是否 > 0。第一次执行时 L 为 [[frozenset([1]), frozenset([3]), frozenset([2]), frozenset([5])]]。L[k-2]=L[0]=[frozenset([1]), frozenset([3]), frozenset([2]), frozenset([5])]，最后面 k += 1
    while (len(L[k-2]) > 0):
        # print 'k=', k, L, L[k-2]
        Ck = createCk(L[k-2], k) # 例如: 以 {0},{1},{2} 为输入且 k = 2 则输出 {0,1}, {0,2}, {1,2}. 以 {0,1},{0,2},{1,2} 为输入且 k = 3 则输出 {0,1,2}
        # print 'Ck', Ck
        Lk, supportLk  = scanDataSet(D, Ck, minSupport) # 计算候选数据集 CK 在数据集 D 中的支持度，并返回支持度大于 minSupport 的频繁项集Lk
        # 保存所有候选项集的支持度，如果字典没有，就追加元素，如果有，就更新元素
        supportData.update(supportLk )
        if len(Lk) == 0:
            break
        #将频繁项集添加到列表L中记录
        L.append(Lk)
        #逐一增加频繁项集中的元素个数
        k += 1
        # print 'k=', k, len(L[k-2])
    return L, supportData

# 计算可信度（confidence）
def calculationConf(subSet, H, supportData,brl,minConference=0.7):
 # 记录可信度大于最小可信度（minConference）的集合
    prunedH = []
    for conseq in H:
        conf = supportData[subSet]/supportData[subSet - conseq] # 支持度定义
        if conf >= minConference:
            print(subSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((subSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH

# 递归计算频繁项集的规则
def rulesFromConseq(subSet, H, supportData, brl, minConference):
    m = len(H[0])
    #如果频繁项集中每项元素个数大于买m+1,即，可以分出m+1个元素在规则等式右边则执行
    if (len(subSet) > (m+1)):
        #利用函数createCk生成包含m+1个元素的候选频繁项集后件
        Hm = createCk(H, (m+1))
        #计算前件（subSet - Hm）--> 后件（Hm）的可信度，并返回可信度大于minConference的集合
        Hm = calculationConf(subSet,Hm,supportData,brl,minConference)
        #当候选后件集合中只有一个后件的可信度大于最小可信度，则结束递归创建规则
        print ('Hm=', Hm)
        print ('len(Hm)=', len(Hm), 'len(subSet)=', len(subSet))
        # 计算可信度后，还有数据大于最小可信度的话，那么继续递归调用，否则跳出递归
        if (len(Hm) > 1):
            rulesFromConseq(subSet, Hm, supportData, brl, minConference)

# 生成关联规则
def generateRules(L,supportData,minConference = 0.7):
    bigRuleList = []
    for i in range(1,len(L)):        # 获取频繁项集中每个组合的所有元素
        for subSet in L[i]:
            H1 = [frozenset([item]) for item in subSet]            # 组合总的元素并遍历子元素，并转化为 frozenset 集合，再存放到 list 列表中
            if (i > 1):
                rulesFromConseq(subSet, H1, supportData, bigRuleList, minConference)            # 2 个的组合，走 else, 2 个以上的组合，走 if
            else:
                calculationConf(subSet, H1, supportData,bigRuleList,minConference)
    return bigRuleList



if __name__ == "__main__":    
    dataset = loadDataSet()
    print(type(dataset))

    
#    scanDataSet(dataset,createC1(dataset),minSupport=0.5)
    L,returnSupportData = apriori(dataset,minSupport=0.5) 
    l = []
    for Lk in L:
        for freq_set in Lk:
            l.append((freq_set, returnSupportData[freq_set]))
#            print(freq_set, returnSupportData[freq_set])
    print(l)
            