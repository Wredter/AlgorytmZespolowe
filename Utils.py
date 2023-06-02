import numpy as np

from DataClass.mock_data import get_groups, get_courses


def count_rows_nan(array):
    start_idx = None
    end_idx = None
    count = 0
    for idx, row in enumerate(array):
        if np.any(~np.isnan(row)):
            if start_idx is None:
                start_idx = idx
            end_idx = idx
    if start_idx is not None:
        if start_idx - end_idx == 0:
            return 0
        for idx, row in enumerate(array):
            if start_idx <= idx <= end_idx:
                if np.all(np.isnan(row)):
                    count += 1
        return count
    return 0


def get_courses_for_group():
    GCT = []
    for group in get_groups():
        for course in group["courses"]:
            for type in get_courses()[course]["types"]:
                _GCT = [group["id"], course, type]
                GCT.append(_GCT)
    return GCT
