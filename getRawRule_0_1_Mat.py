def getRawRule_0_1_Mat(train_trans_list):
    #时序窗口
    #bedroom
    print('bedroom处理中')
    bed_rule_list,bed_count_list = windowT(train_trans_list[1])
    #bathroom
    print('bathroom处理中')
    bath_rules_list,bath_count_cell = windowT(train_trans_list[2])
