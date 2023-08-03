from pulp import *
import json
def weekly_possible_shifts(l):
    union_set = set()

    # Iterate through each list in the list_of_lists
    for sublist in l:
        # Convert the sublist to a set and take the union with the current union_set
        union_set = union_set.union(set(sublist))

    # Convert the union_set back to a list and return
    return list(union_set)

def get_possible_shifts(opening_hour, closing_hour, min_hours_per_shift, max_hours_per_shift):
    possible_shifts = []
    shift_start = opening_hour

    while shift_start + min_hours_per_shift <= closing_hour:
        shift_end = shift_start + min_hours_per_shift

        while shift_end <= closing_hour and shift_end - shift_start <= max_hours_per_shift:
            possible_shifts.append((shift_start, shift_end))
            shift_end += 1

        shift_start += 1

    return possible_shifts

def check_employee_availability(opening_hours, availability):
    all_hours = set()
    for day, (opening_hour, closing_hour) in opening_hours.items():
        all_hours.update(range(opening_hour, closing_hour + 1))

    available_hours_per_day = {
        day: {hour for employee in availability for hour in range(availability[employee][day][0], availability[employee][day][1] + 1)}
        for day in opening_hours.keys()
    }

    for day, (opening_hour, closing_hour) in opening_hours.items():
        unavailable_hours = all_hours.difference(available_hours_per_day[day])
        unavailable_hours = [hour for hour in unavailable_hours if opening_hour <= hour < closing_hour]
        if unavailable_hours:
            print(f"No employee is available on {day} at hours: {sorted(unavailable_hours)}")
        else:
            print(f"At least one employee is available on {day} at all hours.")

min_weekly_hours = 10
max_weekly_hours = 40
opening = {
    "Monday": (8, 16),
    "Tuesday": (8, 20),
    "Wednesday": (8, 13),
    "Thursday": (8, 17),
    "Friday": (9, 18),
    "Saturday": (10, 15),
    "Sunday": (11, 14)
}
min_weekly_hours = {
    'Employee1': 10,
    'Employee2': 15,
    'Employee3': 12,
    'Employee4': 8,
    'Employee5': 20
}

max_weekly_hours = {
    'Employee1': 40,
    'Employee2': 30,
    'Employee3': 25,
    'Employee4': 20,
    'Employee5': 35
}

availability = {
    'Employee1': {
        'Monday': (8, 20),
        'Tuesday': (8, 20),
        'Wednesday': (8, 13),
        'Thursday': (8, 17),
        'Friday': (8, 18),
        'Saturday': (10, 15),
        'Sunday': (11, 14)
    },
    'Employee2': {
        'Monday': (8, 12),
        'Tuesday': (8, 20),
        'Wednesday': (12, 20),
        'Thursday': (8, 15),
        'Friday': (9, 18),
        'Saturday': (10, 14),
        'Sunday': (11, 14)
    },
    'Employee3': {
        'Monday': (8, 12),
        'Tuesday': (8, 20),
        'Wednesday': (12, 20),
        'Thursday': (8, 15),
        'Friday': (9, 18),
        'Saturday': (10, 14),
        'Sunday': (11, 14)
    }
}

with open('opening.json', 'r') as file:
    opening = json.load(file)
with open('availability.json', 'r') as file:
    availability = json.load(file)
#check_employee_availability(opening_hours=opening, availability=availability)

shifts = dict()
for i in opening.keys():
    opening_hour = opening[i][0]
    closing_hour = opening[i][1]
    shifts[i] = get_possible_shifts(opening_hour=opening_hour, closing_hour=closing_hour, min_hours_per_shift=3, max_hours_per_shift=8)

weekly_shifts = weekly_possible_shifts(list(shifts.values()))
employees = availability.keys()
days = opening.keys()

model = LpProblem(name="Workforce_Optimization", sense=LpMinimize)

x = {}
for i in employees:
    for day in days:
        for shift in weekly_shifts:
            x[i, day, shift] = LpVariable(name=f"x_{i}_{day}_{shift}", cat=LpBinary)

model += lpSum(x[i, day, shift] * (shift[1] - shift[0]) for i in employees for day in days for shift in weekly_shifts)

for i in employees:
    model += lpSum(x[i, day, shift] * (shift[1] - shift[0]) for day in days for shift in weekly_shifts) >= min_weekly_hours[i]
    model += lpSum(x[i, day, shift] * (shift[1] - shift[0]) for day in days for shift in weekly_shifts) <= max_weekly_hours[i]

for i in employees:
    for day in days:
        model += lpSum(x[i, day, shift] for shift in weekly_shifts) <= 1

for i in employees:
    for day in days:
        start, end = availability[i][day]
        for shift in weekly_shifts:
            if  not (start <= shift[0] < shift[1] <= end):
                model += x[i, day, shift] == 0

for day in days:
    for hour in range(opening[day][0], opening[day][1]):
        model += lpSum(x[i, day, shift] for i in employees for shift in weekly_shifts if (hour >= shift[0] and hour < shift[1])) >= 1


model.solve()
assigned_shifts = {}
if LpStatus[model.status] == 'Optimal':
    print("Optimal Solution Found.")
    print(max_weekly_hours)
    print(min_weekly_hours)
    print(opening)
    for i in employees:
        assigned_shifts[i] = {}
        for day in days:
            for shift in weekly_shifts:
                if x[i, day, shift].varValue == 1:
                    start_hour, end_hour = shift[0], shift[1]
                    assigned_shifts[i][day] = (start_hour, end_hour)

# Print the results
    for i, shifts_per_day in assigned_shifts.items():
        print(f"{i} shifts:")
        for day, shift in shifts_per_day.items():
            print(f"   {day}: from {shift[0]} to {shift[1]}")

else:
    print("No feasible solution found.")
