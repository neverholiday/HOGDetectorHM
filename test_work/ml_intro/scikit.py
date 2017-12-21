from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from matplotlib import pyplot as plt
import numpy as np

# Initialize seed permutation
np.random.seed(0) 

iris = datasets.load_iris()
knn = KNeighborsClassifier()

iris_X = iris.data
iris_Y = iris.target

# print iris_X
# set indices list to index data randon
indices = np.random.permutation(len(iris_X))

# randommmmm  !!
iris_X_train = iris_X[indices[:-10]]
iris_Y_train = iris_Y[indices[:-10]]
iris_X_test = iris_X[indices[-10:]]
iris_Y_test = iris_Y[indices[-10:]]

knn.fit(iris_X_train,iris_Y_train)

predict = knn.predict(iris_X_test)

print predict
print iris_Y_test