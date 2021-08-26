import pandas as pd

from osdtr import bbound, predict
from utils import ObjFunction



def test_accuracy_onefold(file, lambs, timelimit):
    """
    Run CART and OSDT
    use all data, only training accuracy
    :param X:
    :param y:
    :param lambs:
    :param file_CART:
    :param file_OSDT:
    :return:
    """
    for lamb in lambs:

        file_train = file
        #file_train = file + '.train' + str(1) + '.csv'
        # file_test = file + '.test' + str(1) + '.csv'

        data_train = pd.DataFrame(pd.read_csv(file_train, sep=";"))

        X_train = data_train.values[:, :-1]
        y_train = data_train.values[:, -1]

         # X_test = data_test.values[:, :-1]
        # y_test = data_test.values[:, -1]

        # CART
        # clf = tree.DecisionTreeClassifier(max_depth=5, min_samples_split=max(math.ceil(lamb * 2 * len(y_train)), 2),
        #                                   min_samples_leaf=math.ceil(lamb * len(y_train)),
        #                                   max_leaf_nodes=math.floor(1 / (2 * lamb)),
        #                                   min_impurity_decrease=lamb
        #                                   )
        # clf = clf.fit(X_train, y_train)
        #
        # nleaves_CART = (clf.tree_.node_count + 1) / 2
        # trainaccu_CART = clf.score(X_train, y_train)
        # testaccu_CART = clf.score(X_test, y_test)
        # print(">>>>>>>>>>>>>>>>> nleaves_CART:", nleaves_CART)
        # print(">>>>>>>>>>>>>>>>> trainaccu_CART:", trainaccu_CART)
        # print(">>>>>>>>>>>>>>>>> testaccu_CART:", testaccu_CART)

        # with open(file_CART, 'a+') as f:
        #     f.write(";".join([str('NA'), str(lamb), str(nleaves_CART), str(trainaccu_CART), str('NA')]) + '\n')

        # OSDT
        leaves_c, prediction_c, dic, nleaves_OSDT, nrule, ndata, totaltime, time_c, COUNT, C_c, trainaccu_OSDT, best_is_cart, clf =\
            bbound(X_train, y_train, lamb=lamb,support=True, incre_support=True, accu_support=True, equiv_points=True,
           lookahead=True, lenbound=False, objfunc=ObjFunction.ExternalPathLength, prior_metric="curiosity", timelimit=timelimit, init_cart=False)

        if nleaves_OSDT >= 16:
            break

# lambs1 = [0.1, 0.05, 0.025, 0.01, 0.005, 0.0025]

# Read in the dataset
compas = '../data/preprocessed/compas-binary.csv'
monk1 = '../data/preprocessed/monk1-train.csv'
monk2 = '../data/preprocessed/monk2-train.csv'
monk3 = '../data/preprocessed/monk3-train.csv'
balance = '../data/preprocessed/balance-scale.csv'
tictactoe = '../data/preprocessed/tic-tac-toe.csv'
car = '../data/preprocessed/car-evaluation.csv'

timelimi1 = 1800
datasets = [monk3,balance,tictactoe,car]
# for file in datasets:
# # file = '../data/preprocessed/monk1-train.csv'
#     test_accuracy_onefold(compas , lambs=[0.005],timelimit=timelimi1)
test_accuracy_onefold(compas , lambs=[0.005],timelimit=timelimi1)