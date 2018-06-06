import numpy as np
def windowForTrain(transMat):
    L_section = 50
    L_window = 10
    N_action = 157
    N_section = transMat.shape[1] / L_section
    N_window = int(L_section / L_window)  #5
    # transaction_list = []
    transaction_list = []
    count_vect_list = []
    rule_weight_list = []
    count_seq_in_section = []

    for i in range(0,N_window,1): #50s为一个视频片段，10秒为一个检测窗口
        # count = 0
        action_seq_list = []
        count_list = []
        section_contain_seq = []

        for j in range(int(i*L_window),int(transMat.shape[1]-L_window*(N_section-i)),L_section):#50秒滑窗
            # transMat = np.array(transMat)
            window_mat = transMat[:,range(j,j+L_window)]

            for c in range(0,L_window,1):#10秒一个时序窗口
                col = window_mat[:,c]
                action_seq_index = [i for i in range(len(col)) if col[i]==1]
                if len(action_seq_index)>1:     #时序窗口内如果有动作（出现标注1）就保存该条视频段
                    action_seq = col
                    #判断规则是否已存在
                    has = 0

                    for k in range(0,len(action_seq_list),1):
                        # if(action_seq_list[k] ==action_seq) == np.ones(len(action_seq),1):
                        if (action_seq_list[k] == action_seq).all():
                            has = 1
                            count_list[k] = count_list[k]+1
                            # temp = section_contain_seq[k]
                            # try:
                            #     temp.append(j)
                            # except:
                            #     temp =
                            section_contain_seq[k].append(j)

                    if(has == 0):
                        # action_seq_list[count] = action_seq
                        action_seq_list.append(action_seq)
                        # count_list[count] = 1
                        count_list.append(1)
                        # count_seq_in_section[count] = 1
                        count_seq_in_section.append(1)
                        temp_scs = [j]
                        # section_contain_seq[count] = temp_scs
                        section_contain_seq.append(temp_scs)
                        # temp.append(temp_scs)
                        # count = count + 1

        # transaction = np.zeros(action_seq_list.shape(1),N_action)
        transaction = np.zeros([len(action_seq_list), N_action])
        times = np.zeros([len(action_seq_list),1])
        # for t in range(1,action_seq_list.shape(1),1):
        for t in range(0,len(action_seq_list),1):
            as_a = action_seq_list[t]
            scs = section_contain_seq[t]
            # scs = temp[t]
            times[t] = len(np.unique(scs))
            # temp = np.array(as)
            transaction[t] = as_a.T
        if transaction.shape[0] > 0:
        # if len(transaction)>0:

            transaction_list.append(transaction)
            count_vect = np.array([count_list]).T
            count_vect_list.append(count_vect)
            rule_weight_list.append(count_vect/(L_window*times))
    return transaction_list,count_vect_list,rule_weight_list


