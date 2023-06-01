import numpy
import pygad
from DataClass.Shedule import ScheduleGenerator, Schedule

function_inputs = [4, -2, 3.5, 5, -11, -4.7]
desired_output = 44


def fitness_func(my_ga_instance, solution: Schedule, solution_idx):
    for day_key in solution.schedule:
        for hour_key in solution.schedule[day_key]:
            for element in solution.schedule[day_key][hour_key]:
                group = element[0]


    return 0


_mySchedules = ScheduleGenerator()
np_test = _mySchedules.generate().schedule.to_numpy_array()
my_schedule = Schedule.to_schedule(np_test)
print("koniec")


