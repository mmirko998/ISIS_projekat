import math
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

class Scorer:
    def get_score(self, trainY, trainPredict, testY, testPredict):
        trainScore = math.sqrt(mean_squared_error(trainY, trainPredict))
        testScore = math.sqrt(mean_squared_error(testY, testPredict))
        return trainScore, testScore
    
    def getMapeScore(self, trainY, trainPredict, testY, testPredict):
        trainScore = mean_absolute_percentage_error(trainY, trainPredict)
        testScore = mean_absolute_percentage_error(testY, testPredict) * 100
        return trainScore, testScore