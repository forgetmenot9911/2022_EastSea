from sklearn.ensemble import RandomForestRegressor
from sklearn import datasets,model_selection
import numpy as np
import matplotlib.pyplot as plt
'''
RandomForestRegressor(n_estimators=10,   #  数值型参数，默认值为100，此参数指定了弱分类器的个数。设置的值越大，精确度越好，但是当 n_estimators 大于特定值之后，带来的提升效果非常有限。
				      criterion='mse',   # 其中，参数criterion 是字符串类型，默认值为 ‘mse’，是衡量回归效果的指标。可选的还有‘mae’ 。
				      max_depth=None,    # 数值型，默认值None。这是与剪枝相关的参数，设置为None时，树的节点会一直分裂，直到：（1）每个叶子都是“纯”的；（2）或者叶子中包含于min_sanples_split个样本。推荐从 max_depth = 3 尝试增加，观察是否应该继续加大深度。
				      min_samples_split=2,  # 数值型，默认值2，指定每个内部节点(非叶子节点)包含的最少的样本数。与min_samples_leaf这个参数类似，可以是整数也可以是浮点数。
				      min_samples_leaf=1,  # 数值型，默认值1，指定每个叶子结点包含的最少的样本数。参数的取值除了整数之外，还可以是浮点数，此时（min_samples_leaf * n_samples）向下取整后的整数是每个节点的最小样本数。此参数设置的过小会导致过拟合，反之就会欠拟合。
				      min_weight_fraction_leaf=0.0,  # (default=0) 叶子节点所需要的最小权值
				      max_features='auto',   # 可以为整数、浮点、字符或者None，默认值为None。此参数用于限制分枝时考虑的特征个数，超过限制个数的特征都会被舍弃。
				      max_leaf_nodes=None,   # 数值型参数，默认值为None，即不限制最大叶子节点数。这个参数通过限制树的最大叶子数量来防止过拟合，如果设置了一个正整数，则会在建立的最大叶节点内的树中选择最优的决策树。
				      min_impurity_split=1e-07, # float, optional (default=0.)如果节点的分裂导致不纯度的减少(分裂后样本比分裂前更加纯净)大于或等于min_impurity_decrease，则分裂该节点。
				      bootstrap=True,        # 是否有放回的采样。
				      oob_score=False,       #  oob（out of band，带外）数据，即：在某次决策树训练中没有被bootstrap选中的数据
				      n_jobs=1,              # 并行job个数。
				      random_state=None,      # # 随机种子
				      verbose=0,          # (default=0) 是否显示任务进程
				      warm_start=False)   # 热启动，决定是否使用上次调用该类的结果然后增加新的。
'''
def load_data_regression():
    diabetes=datasets.load_diabetes()
    return model_selection.train_test_split(diabetes.data, diabetes.target, test_size=0.25, random_state=0)
def test_RandomForestRegressor_max_features(*data):
    '''
    测试 RandomForestRegressor 的预测性能随  max_features 参数的影响

    :param data:  可变参数。它是一个元组，这里要求其元素依次为：训练样本集、测试样本集、训练样本的值、测试样本的值
    :return: None
    '''
    X_train,X_test,y_train,y_test=data
    max_features=np.linspace(0.01,1.0)
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    testing_scores=[]
    training_scores=[]
    for max_feature in max_features:
        regr=RandomForestRegressor(n_estimators=10, max_depth=5, max_features=max_feature)
        regr.fit(X_train,y_train)
        training_scores.append(regr.score(X_train,y_train))
        testing_scores.append(regr.score(X_test,y_test))
    ax.plot(max_features,training_scores,label="Training Score")
    ax.plot(max_features,testing_scores,label="Testing Score")
    ax.set_xlabel("max_feature")
    ax.set_ylabel("score")
    ax.legend(loc="lower right")
    ax.set_ylim(0,1.05)
    plt.suptitle("RandomForestRegressor")
    # 设置 X 轴的网格线，风格为 点画线
    plt.grid(axis='x',linestyle='-.')
    plt.savefig('./pic/RandomForest')
if __name__=='__main__':
    X_train,X_test,y_train,y_test=load_data_regression() # 获取回归数据
    test_RandomForestRegressor_max_features(X_train,X_test,y_train,y_test)