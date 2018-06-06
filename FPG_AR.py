import scipy.io
import numpy as np
# import downsample
# def loadSimpDat():
#     # Train_sorted = scipy.io.loadmat('Train_sorted.mat')
#     # # print(Train_sorted['tempdescr'])
#     # simDat = Train_sorted['tempdescr']
#     simpDat = [['r', 'z', 'h', 'j', 'p'],
#                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
#                ['z'],
#                ['r', 'x', 'n', 'o', 's'],
#                ['y', 'r', 'x', 'z', 'q', 't', 'p'],
#                ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
#     return simpDat


# 用于实现列表到字典的转换过程
def createInitSet(dataSet):  # 把每条事务记录由列表转换为frozenset类型，并且其键值对应的值为1。
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0) + 1
        # retDict[trans] = retDict.get(trans, 0) + 1
    return retDict


# 构建FP树的类定义
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None  # 用于链接相似的元素项。
        self.parent = parentNode  # needs to be updated，指向当前节点的父节点。
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):  # 用于将树以文本的形式显示
        print('  ' * ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind + 1)  # 递归调用disp（）

def createTree(dataSet, minSup): #create FP-tree from dataset but don't mine
    headerTable = {}
    #go over dataSet twice
    for trans in dataSet:#first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
            # print('headerTable!:',headerTable)  #第一次统计个数
    for k in list(headerTable.keys()):  #remove items not meeting minSup
        if headerTable[k] < minSup:
            del(headerTable[k])
            # print('headerTable2：',headerTable) #根据支持度第二次统计
    freqItemSet = set(headerTable.keys()) #频繁1-项集
   # print('freqItemSet: ',freqItemSet)
   # print('-------------------------------------')
    if len(freqItemSet) == 0: return None, None  #if no items meet min support -->get out
   # print('headerTable: ',headerTable)
   # print('-------------------------------------')
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link
   # print('headerTable: ',headerTable)

    retTree = treeNode('Null Set', 1, None) #create tree
    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = {}
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            #对当前事项集按频次排序
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
    return retTree, headerTable #return tree and header table

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table 
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(nodeToTest, targetNode):   #this version does not use recursion
    while (nodeToTest.nodeLink != None):    #Do not use recursion to traverse a linked list!
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode
        
def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
    
def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]    #(sort header table by support)
    for basePat in bigL:  #start from bottom of header table
        newFreqSet = preFix.copy()
        ############
       # newFreqSet.add((basePat,headerTable[basePat][0]))
        newFreqSet.add(basePat)
        ############
        #print 'finalFrequent Item: ',newFreqSet    #append to set
        freqItemList.append([newFreqSet,headerTable[basePat][0]])
           
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        #print 'condPattBases :',basePat, condPattBases
        #2. construct cond FP-tree from cond. pattern base
        myCondTree, myHead = createTree(condPattBases, minSup)#cond. FP tree
        #print 'head from conditional tree: ', myHead
        if myHead != None: #3. mine cond. FP-tree
            #print 'conditional tree for: ',newFreqSet
            #myCondTree.disp(1)


            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
    return freqItemList, minSup

# def loadData(i):
#     return transaction_list[i]

# def createInitSet(dataSet):
#     retDict = {}
#     for trans in dataSet:
#         retDict[frozenset(trans)] = retDict.get(frozenset(trans), 0) + 1
#     return retDict
#
def FP_Growth(data, minSup):
    initSet = createInitSet(data)
    # initSet= loadSimpDat(data)
    myFPtree, myHeaderTab = createTree(initSet, minSup)
    #myFPtree.disp()
    myFreqList = []
    myFreqList, tminSup = mineTree(myFPtree, myHeaderTab, minSup, set([]), myFreqList)
    # rules = findRules(myFreqList,min_conf)
    # return myFreqList
    return myFreqList, tminSup

def findRules(myFreqList,min_conf, minsup):
    freq_item_set_dict={}
    freq_item_set=[]
    max_len=0
    for i in range(len(myFreqList)):#for each [frequentSet,support] in myFreqList
        freq_item_set_dict[frozenset(myFreqList[i][0])]=myFreqList[i][1]
        # freq_item_set_dict[myFreqList[i][0]] = myFreqList[i][1]
        freq_item_set.append(frozenset(myFreqList[i][0]))
        # freq_item_set.append(myFreqList[i][0])
        if len(frozenset(myFreqList[i][0]))>max_len:
        # if len(myFreqList[i][0])>max_len:
            max_len = len(frozenset(myFreqList[i][0]))
            # max_len = len(myFreqList[i][0])
    freq_item_set_list=[[] for i in range(max_len)]#index 0:频繁1-项集；index 1：频繁2-项集；以此类推
    for s in freq_item_set:
        size = len(s)
        freq_item_set_list[size-1].append(s)

    #print(len(myFreqList))

    rules=[]
    for i in range(max_len-1):
        slist1 = freq_item_set_list[i]
       # print slist1
        for j in range(i+1,max_len):
            slist2 = freq_item_set_list[j]
           # print slist2
            for s1 in slist1:
                for s2 in slist2:
                   # print s1, s2
                    #conf = freq_item_set_dict[s2]/float(freq_item_set_dict[s1])
                    if s1.issubset(s2):                   
                        conf = freq_item_set_dict[s2]/float(freq_item_set_dict[s1])
                        if conf >= min_conf:
                            rules.append([[s1,s2-s1],minsup,conf*100])

    # FreqItemsets = FP_Growth(myFreqList,minSup)
    return rules


# dataFile = 'Train_sorted.mat'
# data = scio.loadmat(dataFile)
# print(data)
######Train_sorted = scipy.io.loadmat('Train_sorted.mat')
# print(Train_sorted)
# Train_sorted['descr'] = np.array(Train_sorted['tempdescr']).T
# Train_sorted['label'] = np.array(Train_sorted['templabel']).T
# Train_sorted.descr = Train_sorted.get('descr')
######print(Train_sorted['tempdescr'])

# #test

# # print(FP_Growth(simDat))
# simDat = downsample.loadSimpDat()
# initSet = createInitSet(simDat)
# print('iniset:',initSet)
# myFPtree,myHeaderTab = createTree(initSet,7)
# myFPtree.disp()
# print('myHeaderTab:',myHeaderTab)
# freqItems=[]
# mineTree(myFPtree, myHeaderTab, 7, set([]), freqItems)
# print('freqItems:',freqItems)
# myFreList = FP_Growth(simDat,7)
# print('myFreList:',myFreList)
# # for fit_conf in np.arange(0.1,1.1,0.1):
#     print("当置信度为：",fit_conf)
#     rules = findRules(myFreList,fit_conf)
#     print('rules:',rules)
#
# data = loadSimpDat()
# print(createInitSet(data))
# print(FP_Growth(data,2))
# myFrelist, minsup = FP_Growth(data,2)
# print(myFrelist)
# rules = findRules(myFrelist,0.4, minsup)
# print(rules)
# #

#
# # Train_sorted_descr = np.loadtxt('Train2_X.txt')
# print(Train_sorted_descr)

# # data = loadSimpDat()
# # print(data)
# result = createInitSet(data)
# print(data)

# data = loadSimpDat()
# fre,s = FP_Growth(data,2)