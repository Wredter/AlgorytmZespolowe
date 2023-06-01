import random

import numpy as np

from DataClass.mock_data import get_groups, get_rooms, get_courses, get_teachers

all_days = ["mon", "tues", "wed", "thurs", "fri"]
all_hours = ["8:15-9:45", "10:15-11:45", "12:15-13:45", "14:15-15:45", "16:15-17:45", "18:15-19:45"]


class Schedule:
    schedule = []

    def __init__(self):
        self.set_blanc_schedule()

    def set_blanc_schedule(self):
        self.schedule = {
            "mon": {
                "8:15-9:45": [],
                "10:15-11:45": [],
                "12:15-13:45": [],
                "14:15-15:45": [],
                "16:15-17:45": [],
                "18:15-19:45": [],
            },
            "tues": {
                "8:15-9:45": [],
                "10:15-11:45": [],
                "12:15-13:45": [],
                "14:15-15:45": [],
                "16:15-17:45": [],
                "18:15-19:45": [],
            },
            "wed": {
                "8:15-9:45": [],
                "10:15-11:45": [],
                "12:15-13:45": [],
                "14:15-15:45": [],
                "16:15-17:45": [],
                "18:15-19:45": [],
            },
            "thurs": {
                "8:15-9:45": [],
                "10:15-11:45": [],
                "12:15-13:45": [],
                "14:15-15:45": [],
                "16:15-17:45": [],
                "18:15-19:45": [],
            },
            "fri": {
                "8:15-9:45": [],
                "10:15-11:45": [],
                "12:15-13:45": [],
                "14:15-15:45": [],
                "16:15-17:45": [],
                "18:15-19:45": [],
            }
        }

    def add_position(self, GCtTR: list, day: str, hours: str):
        self.schedule[day][hours].append(GCtTR)

    def to_numpy_array(self):
        max_classes = 0
        for day_key in self.schedule:
            for hour_key in self.schedule[day_key]:
                curr = len(self.schedule[day_key][hour_key])
                if curr > max_classes:
                    max_classes = curr
        np_schedule = np.empty((5, 6, max_classes, 5), dtype=float)
        np_schedule.fill(np.nan)
        for idx_day, day_key in enumerate(self.schedule):
            for idx_hour, hour_key in enumerate(self.schedule[day_key]):
                for idx_GCtTR, GCtTR in enumerate(self.schedule[day_key][hour_key]):
                    for idx, element in enumerate(GCtTR):
                        np_schedule[idx_day, idx_hour, idx_GCtTR, idx] = element["id"]
        return np_schedule

    @staticmethod
    def to_schedule(array: np.array):
        new_schedule = Schedule()
        for day_idx, day in enumerate(array):
            for hour_idx, hour in enumerate(day):
                for GCtTR_idx, GCtTR in enumerate(hour):
                    if not np.any(np.isnan(GCtTR), axis=0):
                        temp_GCtTR = [get_groups()[int(GCtTR[0])], get_courses()[int(GCtTR[1])], {"id": int(GCtTR[2])},
                                      get_teachers()[int(GCtTR[3])], get_rooms()[int(GCtTR[4])]]
                        new_schedule.add_position(temp_GCtTR, all_days[day_idx], all_hours[hour_idx])
        return new_schedule


class ScheduleGenerator:
    def __init__(self, teachers=None, courses=None, groups=None, rooms=None):
        self.schedule = Schedule()
        self.teachers = teachers if teachers else get_teachers()
        self.groups = groups if groups else get_groups()
        self.courses = courses if courses else get_courses()
        self.rooms = rooms if rooms else get_rooms()

    def generate(self):
        self.schedule.set_blanc_schedule()
        for group in self.groups:
            group_courses = group["courses"]
            for course in group_courses:
                possible_teachers = []
                for teacher in self.teachers:
                    if course in teacher["courses"]:
                        possible_teachers.append(teacher)
                for _type in self.courses[course]["types"]:
                    possible_rooms = []
                    for room in self.rooms:
                        if _type == 1:
                            if room["room_type"] == 1:
                                possible_rooms.append(room)
                        else:
                            possible_rooms.append(room)

                    schedule_item = [group, self.courses[course], {"id": _type}, random.choice(possible_teachers),
                                     random.choice(possible_rooms)]
                    self.schedule.add_position(schedule_item, random.choice(all_days), random.choice(all_hours))
        return self
