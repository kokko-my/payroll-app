import datetime, calendar

def convert_time_to_float(hour, minute):
    return hour + (minute / 60)

def convert_float_to_time(time):
    hour = int(time)
    minute = (time - int(time)) * 60
    return hour, minute

def get_now_year():
    return datetime.datetime.now().year

def get_now_month():
    return datetime.datetime.now().month

def get_now_day():
    return datetime.datetime.now().day

def get_days_in_month(year, month):
    return calendar.monthrange(year, month)[1]
