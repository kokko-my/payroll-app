# payroll.py
import abc

class Salary(metaclass=abc.ABCMeta):
    def __init__(self, hourly_wage, start_time, end_time):
        # time ex: 17時半 -> 17.5
        self.hourly_wage = hourly_wage
        self.start_time = start_time
        self.end_time = end_time
        if self.end_time < self.start_time:
            self.end_time += 24

    @abc.abstractmethod
    def calc_salary(self):
        pass

class NormalSalary(Salary):
    # 通常の時給で計算
    def calc_salary(self):
        start_time = self.start_time
        end_time = self.end_time
        return self.hourly_wage * (end_time - start_time)

class NightSalary(Salary):
    # 深夜帯の時給で計算
    NIGHT_START_TIME = 22.0
    NIGHT_END_TIME = 5.0
    NIGHT_SURCHARGE_RATE = 0.25

    def __cutout_night_worktime(self):
        start_time = self.start_time
        end_time = self.end_time
        if self.NIGHT_END_TIME <= start_time <= self.NIGHT_START_TIME:
            if end_time <= self.NIGHT_START_TIME:
                return None, None
            elif end_time <= self.NIGHT_END_TIME + 24:
                return self.NIGHT_START_TIME, end_time
            else:
                return self.NIGHT_START_TIME, self.NIGHT_END_TIME + 24
        else:
            if end_time <= self.NIGHT_END_TIME + 24:
                return start_time, end_time
            else:
                return start_time, self.NIGHT_END_TIME + 24

    def calc_salary(self):
        start_time, end_time = self.__cutout_night_worktime()
        if start_time == None and end_time == None:
            return 0
        return self.hourly_wage * self.NIGHT_SURCHARGE_RATE * (end_time - start_time)

class OvertimeSalary(Salary):
    # 時間外労働の時給で計算
    LEGAL_WORKING_HOURS = 8.0
    OVERTIME_SURCHARGE_RATE = 0.25

    def calc_salary(self, break_time):
        start_time = self.start_time
        end_time = self.end_time
        if end_time - start_time <= self.LEGAL_WORKING_HOURS + break_time:
            return 0
        return self.hourly_wage * self.OVERTIME_SURCHARGE_RATE \
            * (end_time - start_time - self.LEGAL_WORKING_HOURS - break_time)

def calc_total_salary(hourly, start_time, end_time, break_start_time, break_end_time):
    return NormalSalary(hourly, start_time, end_time).calc_salary() \
        + NightSalary(hourly, start_time, end_time).calc_salary() \
        + OvertimeSalary(hourly, start_time, end_time).calc_salary(break_end_time - break_start_time) \
        - (
            NormalSalary(hourly, break_start_time, break_end_time).calc_salary() \
            + NightSalary(hourly, break_start_time, break_end_time).calc_salary()
        )
