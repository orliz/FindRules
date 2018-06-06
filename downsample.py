import scipy.io as sio
import numpy as np
def loadSimpDat():

    train = sio.loadmat('Train_157.mat')
    descr = train['train_157_dscr']
    label = train['train_157_label']
    # print(descr)
    # print(label)


    # index = np.argwhere(descr == 1)
    # print(index)
    # rank = index[:,1]
    # print(rank)

    simDat = []
    lis    = []
    # dic = dict()
    for j in range(10):
        # j = 0
        for i in range(156):
         if descr[i][j] == 1:
            # simDat.append(i)
            lis.append(i)
            # dic[j] = simDat
         # lis.append(simDat)

        simDat.append(lis)
        lis = list()
         # print(lis)
        # return simDat
        # print(simDat)
    return simDat
print(loadSimpDat())