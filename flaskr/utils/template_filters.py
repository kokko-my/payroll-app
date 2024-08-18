def convert_float_to_time(time):
    return f'{int(time) :02}時{int((time - int(time)) * 60) :02}分'
