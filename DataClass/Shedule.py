import random

from DataClass.mock_data import get_groups, get_rooms, get_courses, get_teachers

all_days = ["mon", "tues", "wed", "thurs", "fri"]
all_hours = ["8:15-9:45", "10:15-11:45", "12:15-13:45", "14:15-15:45", "16:15-17:45", "18:15-19:45", ]


class Schedule:
    def __init__(self):
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

    # def __str__(self):
    #     for day_key in self.schedule:
    #         for hour_key in self.schedule[day_key]:


class ScheduleGenerator:
    def __init__(self, teachers=None, courses=None, groups=None, rooms=None):
        self.schedule = Schedule()
        self.teachers = teachers if teachers else get_teachers()
        self.groups = groups if groups else get_groups()
        self.courses = courses if courses else get_courses()
        self.rooms = rooms if rooms else get_rooms()

    def generate(self):
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

                    schedule_item = [group, course, _type, random.choice(possible_teachers),
                                     random.choice(possible_rooms)]
                    self.schedule.add_position(schedule_item, random.choice(all_days), random.choice(all_hours))

