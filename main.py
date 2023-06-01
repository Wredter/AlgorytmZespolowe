import numpy as np

from DataClass.Shedule import ScheduleGenerator
from DataClass.mock_data import get_groups


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

    # sprawdzamy parametry rozwiązania w pierwszej kolejności okienka
    for group_idx, group in enumerate(get_groups()):
        group_plan = np.copy(solution)
        group_plan[~(group_plan[:, :, :, :, 0] == group["id"])] = np.nan
        print("krok")
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
            rows_to_check = np.transpose(rows_to_check)
            for idx, row in enumerate(rows_to_check):
                row_uniq = np.unique(row)
                if row_uniq.shape[0] != row.shape[0]:
                    return False
            # a = np.unique(rows_to_check, axis=1)
            # if np.unique(rows_to_check, axis=0).shape[0] != rows_to_check.shape[0]:
            #     return False
    for group_idx, group in enumerate(get_groups()):
        group_plan = np.copy(solution)
        group_plan[~(group_plan[:, :, :, 0] == group["id"])] = np.nan
        print("krok")
        for day in group_plan:
            pass
    return True


dobre = 0
zle = 0
test_dict = {}
_mySchedules = ScheduleGenerator()
while dobre == 0:
    np_test = _mySchedules.generate().schedule.to_numpy_array()
    test = validify(np_test)
    if test:
        dobre += 1
    else:
        zle += 1
    print(zle)
