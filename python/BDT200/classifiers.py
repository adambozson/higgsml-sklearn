from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

class BoostedDecisionTree(AdaBoostClassifier):
    def __init__(self, n_estimators=200, learning_rate=1.0, algorithm='SAMME',
                 splitter='random', max_features=None, max_depth=None,
                 min_weight_fraction_leaf=.05, class_weight=None):

        DT = DecisionTreeClassifier(splitter=splitter,
                                    max_features=max_features,
                                    max_depth=max_depth,
                                    min_weight_fraction_leaf=min_weight_fraction_leaf,
                                    class_weight=class_weight)

        super(BoostedDecisionTree, self).__init__(base_estimator=DT,
                                                 n_estimators=n_estimators,
                                                 algorithm=algorithm)
