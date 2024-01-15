class DataModel:
    year = None
    month = None
    day = None
    hour = None
    temperature = None 
    feels_like = None 
    humidity = None 
    wind_speed = None
    cloud_cover = None 
    week_day = None 
    isDaylight = None 
    load = None

    def __init__(self, year, month, day, hour, temperature, feels_like, humidity, wind_speed,
                 cloud_cover, week_day, isDaylight, load):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.temperature = temperature 
        self.feels_like = feels_like 
        self.humidity = humidity 
        self.wind_speed = wind_speed
        self.cloud_cover = cloud_cover 
        self.week_day = week_day 
        self.isDaylight = isDaylight 
        self.load = load