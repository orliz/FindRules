import loadData
import dataDivide
import getRawSeq_0_1_Mat
import windowForTrain
import classification3
from FPG_AR import *
# from project.FPG_AR import findRules
import numpy as np
import random

#pretrain
train_rate = 0.8
#载入数据
bed_trans, bath_trans, kitchen_trans ,living_trans,home_trans = loadData.loadData()
trans_list = [bed_trans, bath_trans, kitchen_trans ,living_trans,home_trans]

#获取train/test
# project.dataDivide.dataDvide(trans_list ,0.4)
train_trans_list,test_trans_list = dataDivide.dataDivide(trans_list,train_rate)
transactions_list,rule_count_list,weight_list = getRawSeq_0_1_Mat.getRawSeq_0_1_Mat(train_trans_list)
# myFreqList = FP_Growth(transactions_list,5)

section = 50
window = 10

accu_mat_list = [[],[],[],[],[]]
# predict_rt_list = [np.zeros([1,int(len(test_trans_list[0])/50)]),np.zeros([1,int(len(test_trans_list[1])/50)]),np.zeros([1,int(len(test_trans_list[2])/50)]),np.zeros([1,int(len(test_trans_list[3])/50)]),np.zeros([1,int(len(test_trans_list[4])/50)])]
predict_rt_list = [np.zeros([1,int(test_trans_list[0].shape[1]/50)]),np.zeros([1,int(test_trans_list[1].shape[1]/50)]),np.zeros([1,int(test_trans_list[2].shape[1]/50)]),np.zeros([1,int(test_trans_list[3].shape[1]/50)]),np.zeros([1,int(test_trans_list[4].shape[1]/50)])]


class_list = ['bed','bath','kitchen','living','home']
bed_para = [2.5,7,0.5,0.2,0.65,0.05]
bath_para =  [2.5,7,0.5,0.2,0.65,0.05]
kitchen_pata =  [2.5,7,0.5,0.2,0.65,0.05]
living_para =  [2.5,7,0.5,0.2,0.65,0.05]
home_para =  [2.5,7,0.5,0.2,0.65,0.05]
para_length = 10
para_set_list =[bed_para,bath_para,kitchen_pata,living_para,home_para]
train_rules_list = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
motion_result_list = [[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]
# resulttype = np.dtype({
#     'names':['rule', 'support', 'conf'],
#     'formats': ['str', 'f', 'f']
# })
# train_rules_list = np.array([5,5,], dtype=resulttype)

#获取动作序列
for i in range(0,len(transactions_list),1):
    for p in range(0,5,1):
        temp = transactions_list[i][p]
        for t in range(0,temp.shape[0]):
        # if temp.shape[0]>500:
        #     line = range(0,temp.shape[0])
        #     line_part = random.sample(line,500)
        # else:
        #     line = range(0,temp.shape[0])
        #     line_part = random.sample(line,temp.shape[0])
        # for t in line_part:
            motion = temp[t]
            # motion = random.sample(t)
            motion_result = [s for s in range(len(motion)) if motion[s]==1]
            motion_result_list[i][p].append(motion_result)



for c_index in range(0,para_length,1,):
    for s_index in range(0,para_length,1):
        for p in range(0,len(para_set_list),1):
            for w in range(0,int(section/window),1):
                # s = para_set_list[p][0] + para_set_list[p][2]*(s_index)
                s = para_set_list[p][0] + para_set_list[p][2]*(s_index)
                c = para_set_list[p][3] + para_set_list[p][5]*(c_index)
                # s = para_set_list[p][0] + para_set_list[p][2]
                # c = para_set_list[p][3] + para_set_list[p][5]
                # myFreqlist,s=FP_Growth(transactions_list[p][w], s)
                myFreqlist,s = FP_Growth(motion_result_list[p][w],s)
                train_r = findRules(myFreqlist,c,s)
                train_rules_list[p][w] = train_r


        total_count = 0
        for clas in range(0,len(class_list),1):
            accu_count = 0

            for j in range(0,len(test_trans_list[clas]),50):
                total_count = total_count + 1
                testSeq = test_trans_list[clas][:,range(j,j+section)]
                [test_transaction_list,test_count_vect_list,test_rule_weight_list] = windowForTrain.windowForTrain(testSeq)
                score = classification3.classification3(test_transaction_list,test_count_vect_list,train_rules_list,weight_list,transactions_list)
                print(score)
                # rt = [i for i in range(len(score)) if score[i]==score.max(0)]
                rt = [i for i in range(len(score)) if score[i] == max(score)]
                if len(rt)>1:
                    rt=-1

                    total_count = total_count-1
                else:
                    rt = rt[0]
                predict_rt_list[clas][0][int(j/50)] = rt


        for x in range(0,len(class_list),1):
            TP = 0
            TN = 0
            for j in range(0,len(class_list),1):
                temp_a = [i for i in range(len(predict_rt_list[j][0])) if predict_rt_list[j][0][i] == x]
                temp_b = [i for i in range(len(predict_rt_list[j][0])) if predict_rt_list[j][0][i] != x]
                temp_c = [i for i in range(len(predict_rt_list[j][0])) if predict_rt_list[j][0][i] == -1]
                temp = len(temp_b)-len(temp_c)
                if x==j:
                    # TP = TP + temp_a.shape[1]
                    # temp_a = np.array(temp_a)
                    # print(type(temp_a))
                    TP = TP + len(temp_a)
                else:
                    # TN = TN + temp.shape[1]
                    TN = TN + temp
            accu = (TP+TN)/total_count
            # accu_mat_list[i][s_index][c_index] = accu
            # accu_mat_list.append(accu)
            accu_mat_list[i] = accu
            # print(accu_mat_list)
            print(accu)
print("finished")


