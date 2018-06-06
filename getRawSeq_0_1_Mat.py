import windowForTrain
def getRawSeq_0_1_Mat(train_trans_list):
    #时序窗口
    print('bedroom处理中')
    [bed_transaction_list,bed_count_vect_list,bed_rule_weight_list] = windowForTrain.windowForTrain(train_trans_list[0])
    # bathroom
    print('bathroom处理中')
    [bath_transaction_list, bath_count_vect_list, bath_rule_weight_list] = windowForTrain.windowForTrain(train_trans_list[1])
    print('kitchen处理中')
    [kitchen_transaction_list, kitchen_count_vect_list, kitchen_rule_weight_list] = windowForTrain.windowForTrain(train_trans_list[2])
    # lvingroom
    print('lvingroom处理中')
    [living_transaction_list, living_count_vect_list, living_rule_weight_list] = windowForTrain.windowForTrain(train_trans_list[3])
    # homeoffice
    print('homeoffice处理中')
    [home_transaction_list, home_count_vect_list, home_rule_weight_list] = windowForTrain.windowForTrain(train_trans_list[4])

    result_transaction_list = [bed_transaction_list, bath_transaction_list, kitchen_transaction_list,living_transaction_list, home_transaction_list]
    result_rule_count_list = [bed_count_vect_list, bath_count_vect_list, kitchen_count_vect_list,living_count_vect_list, home_count_vect_list]
    result_weight_list = [bed_rule_weight_list, bath_rule_weight_list, kitchen_rule_weight_list,living_rule_weight_list, home_rule_weight_list]

    return result_transaction_list,result_rule_count_list,result_weight_list