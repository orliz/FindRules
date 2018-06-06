def window(transMat):
    window = 10
    rule_list = []
    count_list = []
    count =1
    for i in range(1,transMat.shape[1]-window,window):

