import copy
import os
import random
from datetime import datetime

import numpy as np
import yaml

from DataClass.mock_data import get_groups, get_rooms, get_courses, get_teachers

all_days = ["mon", "tues", "wed", "thurs", "fri"]
all_hours = ["8:15-9:45", "10:15-11:45", "12:15-13:45", "14:15-15:45", "16:15-17:45", "18:15-19:45"]
empty = {
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


class Schedule:
    schedule = []

    def __init__(self):
        self.set_blanc_schedule()
        self.max_elements = len(get_groups())

    def set_blanc_schedule(self):
        self.schedule = copy.deepcopy(empty) #empty.copy()

    def add_position(self, GCtTR: list, day: str, hours: str):
        self.schedule[day][hours].append(GCtTR)

    def remove_last_added(self, day, hours):
        self.schedule[day][hours] = self.schedule[day][hours][:-1]

    def does_it_fit(self, day, hours):
        if len(self.schedule[day][hours]) < self.max_elements:
            return True
        return False

    def to_numpy_array(self):
        np_schedule = np.empty((5, 6, self.max_elements, 5), dtype=float)
        np_schedule.fill(np.nan)
        for idx_day, day_key in enumerate(self.schedule):
            for idx_hour, hour_key in enumerate(self.schedule[day_key]):
                for idx_GCtTR, GCtTR in enumerate(self.schedule[day_key][hour_key]):
                    for idx, element in enumerate(GCtTR):
                        np_schedule[idx_day, idx_hour, idx_GCtTR, idx] = element["id"]
        return np_schedule

    def validify(self):
        curr_solution = self.to_numpy_array()
        for day in curr_solution:
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
        return True

    def simple_schedule(self):
        my_dict = copy.deepcopy(empty)
        class_type = ["wyklad", "laboratorium", "cwiczenia"]
        for day_key in self.schedule:
            for hour_key in self.schedule[day_key]:
                for element in self.schedule[day_key][hour_key]:
                    simple_element = {
                        "grupa": element[0]["name"],
                        "przedmiot": element[1]["name"],
                        "typ": class_type[element[2]["id"]],
                        "prowadzacy": element[3]["name"],
                        "sala": element[4]["name"]
                    }
                    my_dict[day_key][hour_key].append(simple_element)
        return my_dict

    def save_simple_schedule_per_entity(self):
        np_schedule = self.to_numpy_array()
        group_schedule = {}
        teacher_schedule = {}
        room_schedule = {}

        current_time = datetime.now().strftime("%m_%d_%H_%M")
        os.mkdir(f'Saved_schedules\\{current_time}_all_schedules')

        for group in get_groups():
            group_plan = np.copy(np_schedule)
            group_plan[~(group_plan[:, :, :, 0] == group["id"])] = np.nan
            group_schedule[group["name"]] = group_plan
        for teacher in get_teachers():
            teacher_plan = np.copy(np_schedule)
            teacher_plan[~(teacher_plan[:, :, :, 3] == teacher["id"])] = np.nan
            teacher_schedule[teacher["name"]] = teacher_plan
        for room in get_rooms():
            room_plan = np.copy(np_schedule)
            room_plan[~(room_plan[:, :, :, 4] == room["id"])] = np.nan
            room_schedule[room["name"]] = room_plan

        for group_k in group_schedule:
            schedule = Schedule.to_schedule(group_schedule[group_k])
            simple_schedule = schedule.simple_schedule()
            with open(f'Saved_schedules\\{current_time}_all_schedules\\group_{group_k}_schedule.yaml', "w") as file:
                yaml.dump(simple_schedule, file, indent=3, sort_keys=False)
        for teacher_k in teacher_schedule:
            schedule = Schedule.to_schedule(teacher_schedule[teacher_k])
            simple_schedule = schedule.simple_schedule()
            with open(f'Saved_schedules\\{current_time}_all_schedules\\{teacher_k}_schedule.yaml', "w") as file:
                yaml.dump(simple_schedule, file, indent=3, sort_keys=False)
        for room_k in room_schedule:
            schedule = Schedule.to_schedule(room_schedule[room_k])
            simple_schedule = schedule.simple_schedule()
            with open(f'Saved_schedules\\{current_time}_all_schedules\\{room_k}_schedule.yaml', "w") as file:
                yaml.dump(simple_schedule, file, indent=3, sort_keys=False)

        with open(f'Saved_schedules\\{current_time}_all_schedules\\master_schedule.yaml', 'w') as file:
            yaml.dump(self.simple_schedule(), file, indent=3, sort_keys=False)




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
        dead_end = False
        for group in self.groups:
            group_courses = group["courses"]
            for course in group_courses:
                possible_teachers = []
                for teacher in self.teachers:
                    if course in teacher["courses"]:
                        possible_teachers.append(teacher)
                for _type in self.courses[course]["types"]:
                    possible_days_hours = []
                    possible_rooms = []
                    for day in all_days:
                        for hour in all_hours:
                            possible_days_hours.append([day, hour])
                    for room in self.rooms:
                        if _type == 1:
                            if room["room_type"] == 1:
                                possible_rooms.append(room)
                        else:
                            possible_rooms.append(room)
                    schedule_item = [group, self.courses[course], {"id": _type}, random.choice(possible_teachers),
                                     random.choice(possible_rooms)]
                    valid = False
                    while not valid:
                        if not possible_days_hours:
                            print(f"Can't create plan with current requirements.")
                            dead_end = True
                            for day in all_days:
                                for hour in all_hours:
                                    possible_days_hours.append([day, hour])
                        curr_day_hour = random.choice(possible_days_hours)
                        possible_days_hours.remove(curr_day_hour)
                        if self.schedule.does_it_fit(curr_day_hour[0], curr_day_hour[1]):
                            self.schedule.add_position(schedule_item, curr_day_hour[0], curr_day_hour[1])
                            if self.schedule.validify() or dead_end:
                                valid = True
                            else:
                                self.schedule.remove_last_added(curr_day_hour[0], curr_day_hour[1])
        return self
