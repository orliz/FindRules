import random
import numpy as np
def dataDivide(trans_list ,train_rate):
    section_length = 50
    actions = 157

    bed_trans = trans_list[0]
    bath_trans = trans_list[1]
    kitchen_trans = trans_list[2]
    living_trans = trans_list[3]
    home_trans = trans_list[4]

    # bed_count = len(bed_trans[0])/section_length
    # bath_count = len(bath_trans[1]) / section_length
    # kitchen_count = len(kitchen_trans[2]) / section_length
    # living_count = len(living_trans[3]) / section_length
    # home_count = len(home_trans[4]) / section_length


    bed_count = bed_trans.shape[1]/section_length
    bath_count = bath_trans.shape[1] / section_length
    kitchen_count = kitchen_trans.shape[1] / section_length
    living_count = living_trans.shape[1] / section_length
    home_count = home_trans.shape[1] / section_length

    # bedroom_random_vect = random.randint(0,bed_count-1)
    # bathroom_random_vect = random.randint(0, bath_count - 1)
    # kitchen_random_vect = random.randint(0, kitchen_count - 1)
    # livingroom_random_vect = random.randint(0, living_count - 1)
    # homeoffice_random_vect = random.randint(0, home_count - 1)

    temp_a = range(1, int(bed_count)+1)
    bedroom_random_vect = random.sample(temp_a, int(bed_count))
    bedroom_train_index = bedroom_random_vect[0:int(int(bed_count) * train_rate)]
    bedroom_test_index = bedroom_random_vect[int(int(bed_count) * train_rate):int(bed_count)]

    temp_b = range(1, int(bath_count)+1)
    bathroom_random_vect = random.sample(temp_b, int(bath_count))
    bathroom_train_index = bathroom_random_vect[0:int(int(bath_count) * train_rate)]
    bathroom_test_index = bathroom_random_vect[int(int(bath_count) * train_rate):int(bath_count)]

    temp_c = range(1, int(kitchen_count)+1)
    kitchen_random_vect = random.sample(temp_c, int(kitchen_count))
    kitchen_train_index = kitchen_random_vect[0:int(int(kitchen_count) * train_rate)+1]
    kitchen_test_index = kitchen_random_vect[int(int(kitchen_count) * train_rate)+1:int(kitchen_count)]

    temp_d = range(1, int(living_count)+1)
    livingroom_random_vect = random.sample(temp_d, int(living_count))
    livingroom_train_index = livingroom_random_vect[0:int(int(living_count) * train_rate)+1]
    livingroom_test_index = livingroom_random_vect[int(int(living_count) * train_rate)+1:int(living_count)]

    temp_e = range(1, int(home_count+1))
    homeoffice_random_vect = random.sample(temp_e, int(home_count))
    homeoffice_train_index = homeoffice_random_vect[0:int(int(home_count) * train_rate)+1]
    homeoffice_test_index = homeoffice_random_vect[int(int(home_count) * train_rate) + 1:int(home_count)]

    train_index_list = [bedroom_train_index,bathroom_train_index,kitchen_train_index,livingroom_train_index,homeoffice_train_index]
    test_index_list =  [bedroom_test_index,bathroom_test_index,kitchen_test_index,livingroom_test_index,homeoffice_test_index]
    train_trans_list = []
    test_trans_list = []
    for j in range(0,len(trans_list),1):
        temp_trans = trans_list[j]
        temp_train_index_vect = train_index_list[j]
        temp_test_index_vect = test_index_list[j]
        temp_train_trans = np.zeros([actions,section_length*len(temp_train_index_vect)])
        temp_test_trans = np.zeros([actions,section_length*len(temp_test_index_vect)])

        for k in range(0,len(temp_train_index_vect),1):
            index = temp_train_index_vect[k]
            # temp_train_trans[:,k*section_length:(k+1)*section_length] = temp_trans[:,(index-1)*section_length-1:index*section_length-1]
            temp_train_trans[:,k*section_length:(k+1)*section_length] = temp_trans[:,(index-1)*section_length:index*section_length]

        for p in range(0,len(temp_test_index_vect),1):
            index = temp_test_index_vect[p]
            temp_test_trans[:,p*section_length:(p+1)*section_length] = temp_trans[:,(index-1)*section_length:index*section_length]

        train_trans_list.append(temp_train_trans)
        test_trans_list.append(temp_test_trans)
        # train_trans_list[j] = temp_train_trans
        # test_trans_list[j] = temp_test_trans
    return train_trans_list,test_trans_list


