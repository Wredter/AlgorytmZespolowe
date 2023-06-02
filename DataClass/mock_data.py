teachers = [
    {"id": 0,
     "courses": [0, 1, 2, 3],
     "name": "Dariusz Mroz"},
    {"id": 1,
     "courses": [8, 7, 6, 5],
     "name": "Marek Ksiadz"},
    {"id": 2,
     "courses": [3, 4, 5, 6],
     "name": "Kamil Drama"},
    {"id": 3,
     "courses": [0, 1, 2, 3],
     "name": "Jan Mosiadz"},
    {"id": 4,
     "courses": [8, 7, 6, 5],
     "name": "Marek K"},
    {"id": 5,
     "courses": [3, 4, 5, 6],
     "name": "Kamil D"},
    {"id": 6,
     "courses": [0, 1, 2, 3],
     "name": "Dariusz M"},
    {"id": 7,
     "courses": [8, 7, 6, 5],
     "name": "Marek Ks"},
    {"id": 8,
     "courses": [3, 4, 5, 6],
     "name": "Kamil Dr"},
]
courses = [
    {"id": 0,
     "types": [0, 1, 2],
     "name": "Matematyka"},
    {"id": 1,
     "types": [0, 1],
     "name": "Fizyka"},
    {"id": 2,
     "types": [0],
     "name": "Teoria mechaniki kwantowej"},
    {"id": 3,
     "types": [0, 1],
     "name": "Elektoronika"},
    {"id": 4,
     "types": [0, 1],
     "name": "Podstawy programowania"},
    {"id": 5,
     "types": [0, 1],
     "name": "Projektowanie Zespolowe"},
    {"id": 6,
     "types": [0, 1],
     "name": "Silniki baz danych"},
    {"id": 7,
     "types": [0, 1],
     "name": "Implementacje przemyslowe"},
    {"id": 8,
     "types": [0, 1],
     "name": "Systemy Wbudowane"}
]

# types:
# 0 = wykład w [0,1]
# 1 = labolatorium w [1]
# 2 = ćwiczenia w [0,1]
groups = [
    {"id": 0,
     "courses": [0, 1, 2, 3, 4, 5, 6],
     "name": "I"},
    {"id": 1,
     "courses": [0, 1, 2, 3, 4, 5, 6],
     "name": "II"},
    {"id": 2,
     "courses": [0, 1, 7, 3, 4, 5, 6],
     "name": "III"},
    {"id": 3,
     "courses": [0, 1, 2, 3, 4, 7, 6],
     "name": "IV"},
    {"id": 4,
     "courses": [0, 1, 2, 3, 4, 5, 6],
     "name": "V"},
    {"id": 5,
     "courses": [0, 1, 2, 8, 4, 5, 6],
     "name": "VI"},
    {"id": 6,
     "courses": [0, 1, 2, 3, 4, 7, 8],
     "name": "VI"}
]
rooms = [
    {"id": 0,
     "room_type": 0,
     "name": "101"},
    {"id": 1,
     "room_type": 0,
     "name": "102"},
    {"id": 2,
     "room_type": 1,
     "name": "205"},
    {"id": 3,
     "room_type": 1,
     "name": "206"},
    {"id": 4,
     "room_type": 0,
     "name": "103"},
    {"id": 5,
     "room_type": 0,
     "name": "104"},
    {"id": 6,
     "room_type": 1,
     "name": "207"},
    {"id": 7,
     "room_type": 1,
     "name": "208"},
]


# room_types:
# 0 = sala wykładowa
# 1 = labolatorium_komputerowe

def get_teachers():
    return teachers


def get_courses():
    return courses


def get_groups():
    return groups


def get_rooms():
    return rooms
