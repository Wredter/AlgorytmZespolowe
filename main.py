import numpy as np

from DataClass.Shedule import ScheduleGenerator



def fitness_func(my_ga_instance, solution: np.array, solution_idx):
    for day in solution:
        for hour in day:
            mask = np.isnan(hour)
            hour_no_nans = hour[mask]
            # remove nan representing no classes
            rows_to_check = hour_no_nans[:, [0, 3, 4]]
            # sprawdź czy w ciągu zednej godziny nie odbywają się zajęcia w tej samej sali,
            # dla jednej grupy lub nauczyciela. Wartość wymagana
            if np.unique(rows_to_check, axis=0).shape[0] != rows_to_check.shape[0]:
                return 0
    return 0


def validify(solution: np.array):
    for day in solution:
        for hour in day:
            mask = np.isnan(hour)
            hour_no_nans = hour[~mask]
            hour_no_nans = hour_no_nans.reshape((-1, 5))
            # remove nan representing no classes
            rows_to_check = hour_no_nans[:, [0, 3, 4]]
            # sprawdź czy w ciągu zednej godziny nie odbywają się zajęcia w tej samej sali,
            # dla jednej grupy lub nauczyciela. Wartość wymagana
            if np.unique(rows_to_check, axis=0).shape[0] != rows_to_check.shape[0]:
                return False
    return True


dobre = 0
zle = 0
test_dict = {}
_mySchedules = ScheduleGenerator()
for _ in range(500):
    np_test = _mySchedules.generate().schedule.to_numpy_array()
    test = validify(np_test)
    if test:
        dobre += 1
    else:
        zle += 1
    test_dict[_] = [np_test, test]
print(f"Dobre {dobre}, Zle {zle}")
