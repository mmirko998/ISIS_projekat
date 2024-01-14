from keras.layers import Dense
from keras.models import Sequential
import numpy as np
from tensorflow import keras
from AnnBase import AnnBase

MODEL_NAME = 'model_v0.5'


class AnnRegression(AnnBase):
    
    def GetModel(self):
        model = Sequential()
        if self.number_of_hidden_layers > 0:                                      
           model.add(Dense(self._number_of_neurons_in_first_hidden_layer, input_shape=(1, 15), kernel_initializer=self.kernel_initializer, activation=self.activation_function))
           if self.number_of_hidden_layers > 1:
               for i in range(self.number_of_hidden_layers - 2):
                   model.add(Dense(self.number_of_neurons_in_other_hidden_layers, kernel_initializer=self.kernel_initializer, activation=self.activation_function))
        model.add(Dense(self.number_of_neurons_in_other_hidden_layers, kernel_initializer='he_normal', activation='relu'))
        model.add(Dense(1, kernel_initializer=self.kernel_initializer))
        return model
    
    def GetModelFromPath(self, path):
        model = keras.models.load_model(path)
        return model
    
    def CompileAndFit(self, trainX, trainY):
        self.model = self.GetModel()
        self.model.compile(loss=self.cost_function, optimizer=self.optimizer)
        self.trainX = trainX
        self.model.fit(trainX, trainY, epochs=self.epoch_number, batch_size=self.batch_size_number, verbose=self.verbose)
        self.model.save(MODEL_NAME)
        
    def UseCurrentModel(self, path):
        self.model = self.GetModelFromPath(path)
        
    def GetPredict(self, testX):
        trainPredict = self.model.predict(self.trainX)
        testPredict = self.model.predict(testX)
        return trainPredict, testPredict
    
    def CompileFitPredict(self, trainX, trainY, testX):
        self.compile_and_fit(trainX, trainY)
        return self.get_predict(testX)

    def Predict(self, path, testX):     
        self.use_current_model(path)
        return self.get_predict2(testX)