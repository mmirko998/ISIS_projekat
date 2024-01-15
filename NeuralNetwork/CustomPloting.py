import numpy
import matplotlib.pyplot as plt


class CustomPloting:
    
    def MakePlot(self, collection):
        trainPredictPlot = numpy.empty_like(collection)
        trainPredictPlot[:] = numpy.nan
        trainPredictPlot[0:len(collection)] = collection
        return trainPredictPlot

    def ShowPlots(self, testPredict, testY):
        plot1 = self.MakePlot(testPredict)    
        plot2 = self.MakePlot(testY)
        plt.plot(plot1)
        plt.plot(plot2)
        plt.show()