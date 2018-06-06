import scipy.io as sio
def loadData():
    bed_trans =  sio.loadmat('1_bedroom.mat')
    bed_trans = bed_trans['trans_mat']
    bath_trans = sio.loadmat('2_bathroom.mat')
    bath_trans = bath_trans['trans_mat']
    kitchen_trans = sio.loadmat('3_kitchen.mat')
    kitchen_trans = kitchen_trans['trans_mat']
    living_trans = sio.loadmat('4_livingroom.mat')
    living_trans = living_trans['trans_mat']
    home_trans = sio.loadmat('5_homeoffice.mat')
    home_trans = home_trans['trans_mat']
    return bed_trans, bath_trans, kitchen_trans ,living_trans,home_trans
# bed_trans, bath_trans, kitchen_trans ,living_trans,home_trans = loadDate()
