import datetime, calendar

def convert_time_to_float(hour, minute):
    return hour + (minute / 60)

def get_now_year():
    return datetime.datetime.now().year

def get_now_month():
    return datetime.datetime.now().month

def get_now_day():
    return datetime.datetime.now().day

def get_days_in_month(month):
    _, days_in_month = calendar.monthrange(get_now_year(), month)
    return days_in_month
