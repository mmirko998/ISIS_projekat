import pandas
import pyodbc

from DataModel import DataModel

class Database:
    
    def __init__(self):
        databaseConnection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                                      'Server=DESKTOP-JD4H0K0\SQLEXPRESS;'
                                      'Database=ISIS_project;'
                                      'Trusted_Connection=yes;')
        
        cursor = databaseConnection.cursor()
        
        cursor.execute('DROP TABLE Learning_Data')
        cursor.execute('DROP TABLE Average_Load')
        
        cursor.execute(
	                         'CREATE TABLE Learning_Data ('
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
        print("Table initialised")
        
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
        
        
        querry = 'INSERT INTO Learning_Data' + ' (Year, Month, Day, Hour, Temp, Feelslike, Humidity, WindSpeed, CloudCover, WeeakDay, Daylight, Load) ' \
              'VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
                data.year, data.month, data.day, data.hour, data.temperature, data.feels_like, data.humidity, data.wind_speed, data.cloud_cover, data.week_day, data.daylight, data.load
              )
              
        cursor.execute(querry)
        databaseConnection.commit()
        cursor.close()
        databaseConnection.close()
        
        
    def AddAverageLoadToTable(self, year, month, day, averageLoad, isLearning: bool):
        databaseConnection = self.Connect()
        cursor = databaseConnection.cursor()
        
        querry = 'INSERT INTO Average_Load' + input + ' (Year, Month, Day, AvgerageLoad) ' \
              'VALUES ({}, {}, {}, {})'.format(
                year, month, day, averageLoad
              )
              
        cursor.execute(querry)
        databaseConnection.commit()
        cursor.close()
        databaseConnection.close()
        
    
    
    