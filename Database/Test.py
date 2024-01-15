from DataModel import DataModel
from Database import Database

database = Database()
maxload = database.GetMaxLoad()
minload = database.GetMinLoad()
print(maxload)
print(minload)