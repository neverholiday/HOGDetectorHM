from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from matplotlib import pyplot as plt
import numpy as np

# IRIS data only

class SuperviseLearningClass(object):
    
    def __init__(self,isKnn=False):
        np.random.seed(0)
        self.iris = datasets.load_iris()
        if( isKnn is True):
            self.enableKnnClassifier()
    
    def enableKnnClassifier(self):
        self.knn = KNeighborsClassifier()

    def initialDataIris(self):
        iris_X = self.iris.data
        iris_Y = self.iris.target
        return (iris_X,iris_Y)

    def randomTrainTestIris(self,iris_X,iris_Y):
        indices = np.random.permutation(len(iris_X))
        self.iris_X_train = iris_X[indices[:-10]]
        self.iris_Y_train = iris_Y[indices[:-10]]
        self.iris_X_test = iris_X[indices[-10:]]
        self.iris_Y_test = iris_Y[indices[-10:]]

    def getTrainData(self):
        return (self.iris_X_train,self.iris_Y_train)

    def getTestData(self):
        return (self.iris_X_test,self.iris_Y_test)

    def trainDataIris(self,trainX,trainY):
        self.knn.fit(trainX,trainY)
    
    def predictDataIris(self,testX):
        predictData = self.knn.predict(testX)
        return predictData

def main():
    SLearning = SuperviseLearningClass(isKnn=True)

    iris_X,iris_Y = SLearning.initialDataIris()

    SLearning.randomTrainTestIris(iris_X,iris_Y)

    # Get train and test data
    x_train, y_train = SLearning.getTrainData()
    x_test, y_test = SLearning.getTestData()

    SLearning.trainDataIris(x_train,y_train)
    
    y_Predict = SLearning.predictDataIris(x_test)

    print y_Predict
    print y_test

if __name__ == '__main__':
    main()

