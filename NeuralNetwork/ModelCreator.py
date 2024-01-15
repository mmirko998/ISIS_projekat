from datetime import datetime, timedelta
import os
import time
import numpy
from CustomPloting import CustomPloting
from Scorer import Scorer
from AnnRegression import AnnRegression
from Database.Database import Database
from DataPreparer import DataPreparer
import pandas as pd

NUMBER_OF_COLUMNS = 16
SHARE_FOR_TRAINING = 0.85

class ModelCreator:
    def __init__(self):
        self.database = Database()
        self.modelPath = ''
        self.predictedData = []
        self.predictedDate = None
        
    def StartModelTraining(self, yearFrom, monthFrom, dayFrom, yearTo, monthTo, dayTo):
        self.dataframe = self.LoadData(yearFrom, monthFrom, dayFrom, yearTo, monthTo, dayTo)
        self.preparer = DataPreparer(self.dataframe, NUMBER_OF_COLUMNS, SHARE_FOR_TRAINING)
        trainX, trainY, testX, testY = self.PrepareData()
        
        # make predictions
        Ann_Regression = AnnRegression()
        time_begin = time.time()
        trainPredict, testPredict = Ann_Regression.CompileFitPredict(trainX, trainY, testX)
        time_end = time.time()
        print('Training duration: ' + str((time_end - time_begin)) + ' seconds')

        # invert predictions
        trainPredict, trainY, testPredict, testY = self.preparer.InverseTransform(trainPredict, testPredict)

        self.CalculateError(trainY, trainPredict, testY, testPredict)

        self.Plot(testPredict, testY)
        
        
    def Predict(self, days, yearFrom, monthFrom, dayFrom):
        self.predicted_date = datetime(yearFrom, monthFrom, dayFrom)

        date_to = datetime(yearFrom, monthFrom, dayFrom) + timedelta(days=days - 1)
        self.dataframe = self.LoadTestData(yearFrom, monthFrom, dayFrom, date_to.year, date_to.month, date_to.day) 
                                                                          #SHARE_FOR_TRAINING           
        self.preparer = DataPreparer(self.dataframe, NUMBER_OF_COLUMNS, 0)
        

        testX, testY = self.PrepareTestData()

        # make predictions
        Ann_Regression = AnnRegression()
        time_begin = time.time()
        testPredict = Ann_Regression.Predict(self.GetPath(), testX)

        time_end = time.time()
        print('Test done in duration: ' + str((time_end - time_begin)) + ' seconds')

        # invert predictions
        #trainPredict, trainY, testPredict, testY = self.preparer.inverse_transform(trainPredict, testPredict)
        
        testPredict = numpy.reshape(testPredict, (testPredict.shape[0]))
        
        self.predicted_data = testPredict
        #self.Plot(testPredict, testY)
        rescaled_data, dates = self.ScaleBack()

    def GetCSV(self):
        if self.predicted_data == []:
            return {"error": "Error! No prediction!"}, 400
        
        rescaled_data, dates = self.ScaleBack()
        self.GenerateCSV(rescaled_data, dates)
        return {"data": "OK"}, 200

    def ScaleBack(self):
        max_orig = self.database.GetMaxLoad()
        min_orig = self.database.GetMinLoad()
        max_pred = max(self.predicted_data)
        min_pred = min(self.predicted_data)
        curr_date = self.predicted_date
        dates = []
        rescaled_data = []

        for val in self.predicted_data:
            dates.append(curr_date)
            curr_date += timedelta(hours=1)
            rescaled_data.append(round((max_orig-min_orig) * (val - min_pred) / (max_pred - min_pred) + min_orig, 1))
    
        return rescaled_data, dates

    def GenerateCSV(self, rescaled_data, dates):
        csv_data = {'Timestamp': dates,
                    'Load': rescaled_data}
        df = pd.DataFrame(csv_data)
        column_names = ['Timestamp','Load']
        df.to_csv("result.csv", header=column_names)

    def SetPath(self, path):
        self.path = path

    def GetPath(self):
        return os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models'), self.path)


    def LoadData(self, yearFrom, monthFrom, dayFrom, yearTo, monthTo, dayTo):
        print("Load data started", datetime.now())
        dataframe = self.database.GetDataframe(yearFrom, monthFrom, dayFrom, yearTo, monthTo, dayTo, True)
        print("Load data finished", datetime.now())
        return dataframe

    def LoadTestData(self, yearFrom, monthFrom, dayFrom, yearTo, monthTo, dayTo):
        print("Load data started", datetime.now())
        dataframe = self.database.GetDataframe(yearFrom, monthFrom, dayFrom, yearTo, monthTo, dayTo, False)
        print("Load data finished", datetime.now())
        return dataframe

    def PrepareData(self):
        return self.preparer.PrepareDataForTraining()

    def PrepareTestData(self):
        return self.preparer.PrepareDataForTesting()

    def CalculateError(self, trainY, trainPredict, testY, testPredict):
        scorer = Scorer()
        trainScore, testScore = scorer.get_score(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f RMSE' % (trainScore))
        print('Test Score: %.2f RMSE' % (testScore))
        trainScore, testScore = scorer.getMapeScore(trainY, trainPredict, testY, testPredict)
        print('Train Score: %.2f MAPE' % (trainScore))
        print('Test Score: %.2f MAPE' % (testScore)) 

    def Plot(self, testPredict, testY):
        custom_plotting = CustomPloting()
        custom_plotting.ShowPlots(testPredict, testY)