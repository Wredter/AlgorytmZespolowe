import copy
import pickle
from datetime import datetime

import numpy as np
import pygad
import yaml

from DataClass.Shedule import ScheduleGenerator, Schedule
from DataClass.mock_data import get_groups, get_teachers
from Utils import count_rows_nan, get_courses_for_group


def generations_callback(ga_instance):
    print("Generation:", ga_instance.generations_completed)
    print("Best fitness value:", ga_instance.best_solution()[1])


def fitness_func(my_ga_instance, solution: np.array, solution_idx):
    solution = solution.reshape((5, 6, len(get_groups()), 5))
    for day in solution:
        for hour in day:
            mask = np.isnan(hour)
            hour_no_nans = hour[~mask]
            if hour_no_nans.shape[0] % 5 != 0:
                print("stop")
            hour_no_nans = hour_no_nans.reshape((-1, 5))
            # remove nan representing no classes
            rows_to_check = hour_no_nans[:, [0, 3, 4]]
            # sprawdź czy w ciągu zednej godziny nie odbywają się zajęcia w tej samej sali,
            # dla jednej grupy lub nauczyciela. Wartość wymagana
            rows_to_check = np.transpose(rows_to_check)
            for idx, row in enumerate(rows_to_check):
                row_uniq = np.unique(row)
                if row_uniq.shape[0] != row.shape[0]:
                    return 0
    _GCT = copy.deepcopy(GCT)
    for day in solution:
        for hour in day:
            mask = np.isnan(hour)
            hour_no_nans = hour[~mask]
            hour_no_nans = hour_no_nans.reshape((-1, 5))
            rows_to_check = hour_no_nans[:, [0, 1, 2]]
            for row in rows_to_check:
                temp = [row[0], row[1], row[2]]
                try:
                    _GCT.remove(temp)
                except ValueError:
                    return 0
    if _GCT:
        return 0
    # sprawdzamy parametry rozwiązania w pierwszej kolejności okienka
    group_gaps = []
    teacher_gaps = []
    # policz okienka u wszystkich grup
    for group_idx, group in enumerate(get_groups()):
        group_plan = np.copy(solution)
        group_plan[~(group_plan[:, :, :, 0] == group["id"])] = np.nan
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
    g_gap = sum(group_gaps)
    t_gap = sum(teacher_gaps)
    return (1 / (g_gap + 1)) + (1 / (t_gap + 1))


def custom_swap_mutation(solution, ga_instance: pygad.GA):
    temp = int(solution.shape[0] * ga_instance.mutation_probability)
    solutions_to_mutate = np.random.choice(solution.shape[0], temp, replace=False)
    for idx in solutions_to_mutate:
        m_solution = solution[idx].reshape((5, 6, len(get_groups()), 5))
        random_hour = np.random.choice(m_solution.shape[1], size=2, replace=True)
        random_day = np.random.choice(m_solution.shape[0], size=2, replace=True)
        temp = np.copy(m_solution[random_day[0], [random_hour[0]]])
        m_solution[random_day[0], [random_hour[0]]] = m_solution[random_day[1], [random_hour[1]]]
        m_solution[random_day[1], [random_hour[1]]] = temp
    return solution


def custom_crossover_function(parents, offspring_size, ga_instance):
    offspring = []
    idx = 0
    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

        random_split_point = np.random.choice(range(0, offspring_size[1], 5))

        parent1[random_split_point:] = parent2[random_split_point:]

        offspring.append(parent1)

        idx += 1

    return np.array(offspring)


if __name__ == "__main__":
    my_generator = ScheduleGenerator()
    GCT = get_courses_for_group()
    num_initial_pop = 100
    pop = []
    load_schedules = False
    current_time = datetime.now().strftime("%m_%d_%H_%M")
    schedules_to_load = "Saved_schedules/schedule_06_02_18_23.pkl"
    if load_schedules:
        print("Loading schedules")
        with open(schedules_to_load, 'rb') as file:
            pop = pickle.load(file)
    else:
        print("Generating schedules")
        for _ in range(num_initial_pop):
            schedule = my_generator.generate().schedule.to_numpy_array().flatten()
            print(f"Fitness: {fitness_func(None, schedule, None)}")
            pop.append(schedule)
            print(f"Generated {_}/{num_initial_pop}")
        print("Saving schedules")
        with open(f'Saved_schedules\\schedule_{current_time}.pkl', 'wb') as file:
            pickle.dump(pop, file)

    num_generations = 3000
    num_parents_mating = 4
    population_size = 30
    mutation_probability = 0.05

    parent_selection_type = "sss"
    keep_parents = 1
    print("Looking for best schedule")
    ga_instance = pygad.GA(num_generations=num_generations,
                           stop_criteria=["reach_2.0", "saturate_500"],
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_func,
                           initial_population=pop,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=custom_crossover_function,
                           mutation_type=custom_swap_mutation,
                           mutation_probability=mutation_probability,
                           on_generation=generations_callback
                           )
    ga_instance.run()
    ga_instance.plot_fitness()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    finall_schedule = Schedule.to_schedule(solution.reshape((5, 6, len(get_groups()), 5)))
    if solution_fitness != 0:
        with open(f'Saved_schedules\\finall_schedule_{current_time}.yaml', 'w') as file:
            yaml.dump(finall_schedule.simple_schedule(), file, indent=3, sort_keys=False)
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
