import pandas
import pyodbc

from DatabaseManagement.DataModel import DataModel

class Database:
    
    def __init__(self):
      databaseConnection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                    'Server=DESKTOP-JD4H0K0\SQLEXPRESS;'
                                    'Database=ISIS_project;'
                                    'Trusted_Connection=yes;')
      
      cursor = databaseConnection.cursor()
      """
      cursor.execute('DROP TABLE Learning_Data')
      cursor.execute('DROP TABLE Average_Load')
      
      
      cursor.execute('DROP TABLE Learning_Data_Input')
      cursor.execute('DROP TABLE Average_Load_Input')
      """
      """
      cursor.execute(
                          'CREATE TABLE dbo.Learning_Data ('
                              'Year smallint not null,'
                          'Month tinyint not null,'
                                'Day tinyint not null,'
                                'Hour tinyint not null,'
                            'Temperature real not null,'
                            'Feelslike real not null,'
                            'Humidity real not null,' 
                            'WindSpeed real not null,'
                                'CloudCover real not null,'
                                'WeeakDay tinyint not null,' 
                                'IsDaylight bit not null,'
                            'Load real not null'
                          ')')
      
      cursor.execute(
                          'CREATE TABLE Average_Load ('
                                'Year smallint not null,'
                            'Month tinyint not null,'
                                'Day tinyint not null,'
                            'AvgerageLoad real not null'
                          ')')
      
      cursor.execute(
                          'CREATE TABLE dbo.Learning_Data_Input ('
                              'Year smallint not null,'
                          'Month tinyint not null,'
                                'Day tinyint not null,'
                                'Hour tinyint not null,'
                            'Temperature real not null,'
                            'Feelslike real not null,'
                            'Humidity real not null,' 
                            'WindSpeed real not null,'
                                'CloudCover real not null,'
                                'WeeakDay tinyint not null,' 
                                'IsDaylight bit not null,'
                            'Load real not null'
                          ')')
      
      cursor.execute(
                          'CREATE TABLE Average_Load_Input ('
                                'Year smallint not null,'
                            'Month tinyint not null,'
                                'Day tinyint not null,'
                            'AvgerageLoad real not null'
                          ')')
      print("Tables initialised") 
      """
      databaseConnection.commit()
      
      
      cursor.close()   
      databaseConnection.close()


    def Connect(self):
      print('Connecting')
      return pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                    'Server=DESKTOP-JD4H0K0\SQLEXPRESS;'
                                    'Database=ISIS_project;'
                                    'Trusted_Connection=yes;')
    
    def AddDataToLearningDataTable(self, data: DataModel, isLearning: bool):
      databaseConnection = self.Connect()
      cursor = databaseConnection.cursor()
      
      input = ''
      if isLearning == False:
          input = '_Input'
      
      querry = 'INSERT INTO Learning_Data' + input + ' (Year, Month, Day, Hour, Temp, Feelslike, Humidity, WindSpeed, CloudCover, WeeakDay, Daylight, Load) ' \
            'VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
              data.year, data.month, data.day, data.hour, data.temperature, data.feels_like, data.humidity, data.wind_speed, data.cloud_cover, data.week_day, data.isDaylight, data.load
            )
            
      cursor.execute(querry)
      databaseConnection.commit()
      cursor.close()
      databaseConnection.close()
        
        
    def AddAverageLoadToTable(self, year, month, day, averageLoad, isLearning: bool):
      databaseConnection = self.Connect()
      cursor = databaseConnection.cursor()
      
      input = ''
      if isLearning == False:
          input = 'Input'

      
      querry = 'INSERT INTO Average_Load' + input + ' (Year, Month, Day, AvgerageLoad) ' \
            'VALUES ({}, {}, {}, {})'.format(
              year, month, day, averageLoad
            )
            
      cursor.execute(querry)
      databaseConnection.commit()
      cursor.close()
      databaseConnection.close()
        
    def GetDataframe(self, yearFrom, monthFrom, dayFrom, yearTo, monthTo, dayTo, learningData):
      databaseConnection = self.Connect()
      cursor = databaseConnection.cursor()
      rows = cursor.execute('SELECT * FROM dbo.LearningData')  
      dataFrame = pandas.DataFrame((tuple(t) for t in rows)) 
      cursor.close()
      databaseConnection.close()
      return dataFrame
    
    def GetMaxLoad(self):
      databaseConnection = self.Connect()
      cursor = databaseConnection.cursor()
      
      cursor.execute('SELECT * FROM dbo.Average_Load')
      rows = cursor.fetchall()
      
      maxLoad = 0
      
      for row in rows:
        if row[3] > maxLoad:
          maxLoad = row[3]
      
      return maxLoad
    
    def GetMinLoad(self):
      databaseConnection = self.Connect()
      cursor = databaseConnection.cursor()
      
      cursor.execute('SELECT * FROM dbo.Average_Load')
      rows = cursor.fetchall()
      
      minLoad = rows[0][3]
      
      for row in rows:
        if row[3] < minLoad:
          minLoad = row[3]
      
      return minLoad
    
    