import numpy as np

from DataClass.Shedule import ScheduleGenerator
from DataClass.mock_data import get_groups, get_teachers
from Utils import count_rows_nan


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
    group_gaps = []
    teacher_gaps = []
    # policz okienka u wszystkich grup
    for group_idx, group in enumerate(get_groups()):
        group_plan = np.copy(solution)
        group_plan[~(group_plan[:, :, :, 0] == group["id"])] = np.nan
        print("krok")
        gaps = 0
        for day in group_plan:
            gaps += count_rows_nan(day)
        group_gaps.append(gaps)
    # policz okienka u wszystkich nauczycieli
    for teacher_idx, teacher in enumerate(get_teachers()):
        teacher_plan = np.copy(solution)
        teacher_plan[~(teacher_plan[:, :, :, 3] == teacher["id"])] = np.nan
        gaps = 0
        for day in teacher_plan:
            gaps += count_rows_nan(day)
        teacher_gaps.append(gaps)
    return True


def test_mutation(solution):
    random_hour = np.random.choice(solution.shape[1], size=2, replace=True)
    random_day = np.random.choice(solution.shape[0], size=2, replace=True)
    temp = np.copy(solution[random_day[0], [random_hour[0]]])
    solution[random_day[0], [random_hour[0]]] = solution[random_day[1], [random_hour[1]]]
    solution[random_day[1], [random_hour[1]]] = temp
    return solution


dobre = 0
zle = 0
test_dict = {}
_mySchedules = ScheduleGenerator()
while dobre == 0:
    np_test = _mySchedules.generate().schedule.to_numpy_array()
    np_test_f = np_test.flatten()
    np_test_fb = np_test_f.reshape((5, 6, len(get_groups()), 5))
    test = validify(np_test)
    np_test = test_mutation(np_test)
    if test:
        dobre += 1
    else:
        zle += 1
    print(zle)
