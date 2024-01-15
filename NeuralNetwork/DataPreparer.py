import numpy
from sklearn.preprocessing import MinMaxScaler


class DataPreparer:
        def __init__(self, dataFrame, numberOfColumns, share_for_training):
            self.scaler = MinMaxScaler(feature_range=(0, 1))
            self.datasetOrig = dataFrame.values
            self.datasetOrig = self.datasetOrig.astype('float32')
            self.numberOfColumns = numberOfColumns
            self.predictorColumnNo = self.numberOfColumns - 1
            self.shareForTraining = share_for_training
            
        def PrepareDataForTraining(self):
            dataset = self.scaler.fit_transform(self.datasetOrig)
            trainSize = int(len(dataset) * self.shareForTraining)
            testSize = len(dataset) - trainSize
            train, test = dataset[0:trainSize,:], dataset[trainSize:len(dataset),:]
            print(len(train), len(test))        
            lookBack = self.numberOfColumns(train, lookBack)
            trainX, trainY = self.CreateDataset(train, lookBack)
            testX, testY = self.CreateDataset(test, lookBack)
            trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
            testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
            self.trainX = trainX
            self.trainY = trainY
            self.testX = testX
            self.testY = testY
            return trainX.copy(), trainY.copy(), testX.copy(), testY.copy()
        
        def PrepareDataForTesting(self):
            #dataset = self.scaler.fit_transform(self.datasetOrig)
            dataset = self.datasetOrig
            train_size = int(len(dataset) * self.shareForTraining)
            test_size = len(dataset) - train_size
            train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
            print(len(train), len(test))        
            look_back = self.numberOfColumns
            #trainX, trainY = self.create_dataset(train, look_back)
            testX, testY = self.createTestDataset(test, look_back)
            #trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
            testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
            #self.trainX = trainX
            #self.trainY = trainY
            self.testX = testX
            self.testY = testY
            return testX.copy(), testY.copy()
        
        def InverseTransform(self, trainPredict, testPredict):
            trainPredict = numpy.reshape(trainPredict, (trainPredict.shape[0], trainPredict.shape[1]))
            testPredict = numpy.reshape(testPredict, (testPredict.shape[0], testPredict.shape[1]))
            self.trainX = numpy.reshape(self.trainX, (self.trainX.shape[0], self.trainX.shape[2]))
            self.testX = numpy.reshape(self.testX, (self.testX.shape[0], self.testX.shape[2]))
            trainXAndPredict = numpy.concatenate((self.trainX, trainPredict),axis=1)
            testXAndPredict = numpy.concatenate((self.testX, testPredict),axis=1)
            trainY = numpy.reshape(self.trainY, (self.trainY.shape[0], 1))
            testY = numpy.reshape(self.testY, (self.testY.shape[0], 1))
            trainXAndY = numpy.concatenate((self.trainX, trainY),axis=1)
            testXAndY = numpy.concatenate((self.testX, testY),axis=1)
            trainXAndPredict = self.scaler.inverse_transform(trainXAndPredict)
            trainXAndY = self.scaler.inverse_transform(trainXAndY)
            testXAndPredict = self.scaler.inverse_transform(testXAndPredict)
            testXAndY = self.scaler.inverse_transform(testXAndY)
            trainPredict = trainXAndPredict[:,self.predictor_column_no]
            trainY = trainXAndY[:,self.predictor_column_no]
            testPredict = testXAndPredict[:,self.predictor_column_no]
            testY = testXAndY[:,self.predictor_column_no]
            return trainPredict, trainY, testPredict, testY
        
        def CreateDataset(self, dataset, lookBack):
            dataX, dataY = [], []
            for i in range(len(dataset)-1):
                a = dataset[i, 0:lookBack-1]
                dataX.append(a)
                dataY.append(dataset[i, lookBack-1])
            return numpy.array(dataX), numpy.array(dataY)
        
        def createTestDataset(self, dataset, lookBack):
            dataX, dataY = [], []
            for i in range(len(dataset)):
                a = dataset[i, 0:lookBack-1]
                dataX.append(a)
                dataY.append(dataset[i, lookBack-1])
            return numpy.array(dataX), numpy.array(dataY)