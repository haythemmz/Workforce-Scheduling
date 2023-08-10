from pulp import *
import json
from tools import * 

min_weekly_hours = 10
max_weekly_hours = 40
min_weekly_hours= {
    "Employee1": 5,
    "Employee2": 5,
    "Employee3":5,
    "Employee4": 2,
    "Employee5": 1,
    "Employee6": 1,
    "Employee7": 1,
    "Employee8": 2,
    "Employee9": 1,
    "Employee10": 1
  }

max_weekly_hours ={
    "Employee1": 50,
    "Employee2": 40,
    "Employee3": 40,
    "Employee4": 40,
    "Employee5": 50,
    "Employee6": 40,
    "Employee7": 40,
    "Employee8": 40,
    "Employee9": 50,
    "Employee10": 40
  }


with open('minimum_employees.json', 'r') as file:
    minimum_employees = json.load(file)


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
print(len(employees))






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
        num_employees_required = minimum_employees.get(day, {}).get(str(hour), 0)
        model += lpSum(x[i, day, shift] for i in employees for shift in weekly_shifts if (hour >= shift[0] and hour < shift[1])) >=   num_employees_required


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
