import numpy as np
def classification3(test_video_ac_seq_list,test_ac_seq_count_list,rules_list,weight,raw_seq):

    # class_count = max(len(rules_list[0]),len(rules_list[1]),len(rules_list[2]))
    class_count = len(rules_list)
    # n_windows = test_video_ac_seq_list.shape[1]
    # n_windows = len(test_video_ac_seq_list)
    n_windows = 5
    window_score = np.zeros([class_count,n_windows])

    total_conf_mat = np.zeros([class_count,n_windows])
    avg_conf_mat = np.zeros([class_count,n_windows])
    for i in range(0,class_count,1):
        for j in range(0,n_windows,1):
            #每类置信度平均
            avg_conf_mat[i][j] = np.sum(np.array(rules_list[i][0])[:,2])/len(rules_list[i][0])
            total_conf_mat[i][j] = np.sum(np.array(rules_list[i][0])[:,2])

    #每子段（window）在每类对应子段上的打分

    for j in range(0,n_windows,1):
         # test_ac_seq_count_array = np.array(test_ac_seq_count_list[j])
         # for t in range(1,test_video_ac_seq_list[j].shape(0),1):
         if len(test_video_ac_seq_list)>j:
             for t in range(0,test_video_ac_seq_list[j].shape[0],1):

                 for i in range(0,class_count,1):
                     # for k in range(1,rules_list[i][j].shape(0),1):
                     for k in range(0,len(rules_list[i][j])):
                         has = 1
                         # rule_str = rules_list[i][j][k][1]
                         rule_str = rules_list[i][j][k][0]
                         rule_str_a = list(rule_str[0])
                         rule_str_b = list(rule_str[1])
                         for x in rule_str_b:
                             rule_str_a.append(x)
                             # print(rule_str_a)
                         # rule_str = rule_str.replace('->','')
                         # rule_str = rule_str.replace(',','')
                         # rule_vect = int(rule_str)

                         if len(sorted([i for i in range(len(test_video_ac_seq_list[j][t])) if test_video_ac_seq_list[j][t][i]==1]))== len(sorted(rule_str)):
                            # print('1')
                            if sorted([i for i in range(len(test_video_ac_seq_list[j][t])) if test_video_ac_seq_list[j][t][i]==1])==sorted(rule_str_a):
                                # print('2')
                                # for r in range(1,np.array(raw_seq).shape[0],1):
                                #     temp = raw_seq[i-1]
                                #     temp_a = temp[1][j]
                                #     raw_seq_temp = temp_a[r-1]
                                #     test_video_ac_seq_list_temp = test_video_ac_seq_list[j]
                                #     test_video_ac_seq_list_temp = test_video_ac_seq_list_temp[t-1]
                                #     if raw_seq_temp == test_video_ac_seq_list_temp:
                                #         temp =weight[i]
                                #         temp_a= temp[j]
                                #         w1 = np.array(temp_a)[r]
                                #         count = np.array(test_ac_seq_count_list[j])[t]
                                #         w2 = 1 - (count-w1*10)/(w1*10)
                                #         window_score[i][j] = window_score[i][j] + rules_list[i][j][k][3]*w1*w2
                                for r in range(0,raw_seq[i][j].shape[0],1):
                                    if (raw_seq[i][j][r] == test_video_ac_seq_list[j][t]).all():
                                        # print('3')
                                        w1 = weight[i][j][r]
                                        count = test_ac_seq_count_list[j][t] #?????????????????????????
                                        w2 = 1 - (count-w1*10)/(w1*10)
                                        window_score[i][j] = window_score[i][j] + rules_list[i][j][k][2]*w1*w2


    window_score = window_score/total_conf_mat
    score = window_score.sum(axis=1)
    return score
