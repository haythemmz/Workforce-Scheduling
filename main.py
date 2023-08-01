from pulp import *

def get_possible_shifts(opening_hour, closing_hour, min_hours_per_shift, max_hours_per_shift):
    possible_shifts = []
    shift_start = opening_hour

    # Loop until we reach the closing hour
    while shift_start + min_hours_per_shift <= closing_hour:
        shift_end = shift_start + min_hours_per_shift

        # Loop through all possible shift end times within the maximum hours per shift
        while shift_end <= closing_hour and shift_end - shift_start <= max_hours_per_shift:
            possible_shifts.append((shift_start, shift_end))
            shift_end += 1  # Increment the shift end time

        shift_start += 1  # Increment the shift start time

    return possible_shifts

def weekly_possible_shifts(l):
    union_set = set()

    # Iterate through each list in the list_of_lists
    for sublist in l:
        # Convert the sublist to a set and take the union with the current union_set
        union_set = union_set.union(set(sublist))

    # Convert the union_set back to a list and return
    return list(union_set)

num_employees = 2
opening = {
    "Monday": (8, 16),
    "Tuesday": (8, 21),
    "Wednesday": (8, 13)
    # Add shifts for other days as needed
}
C = 10  # Cost per employee/hour (same for all employees/hours)
min_weekly_hours = 10
max_weekly_hours = 40

availability = {
    'Employee1': {
        'Monday': (8, 20),
        'Tuesday': (8, 14),
        'Wednesday': (8, 12)
    },
    'Employee2': {
        'Monday': (8, 12),
        'Tuesday': (8, 21),
        'Wednesday': (10, 13),
    }
}
shifts=dict()
for i in opening.keys():
    opening_hour=opening[i][0]
    closing_hour=opening[i][1]
    shifts[i]=get_possible_shifts(opening_hour=opening_hour,closing_hour=closing_hour,min_hours_per_shift=3,max_hours_per_shift=8)

weekly_shifts=weekly_possible_shifts(list(shifts.values()))
employees=availability.keys()
days=opening.keys()
model = LpProblem(name="Workforce_Optimization", sense=LpMinimize)

# Decision variables: x[i][day][shift] is a binary variable representing whether employee i is assigned to shift on day
x = {}
for i in employees:
    for day in days:
        for shift in weekly_shifts:
            x[i, day, shift] = LpVariable(name=f"x_{i}_{day}_{shift}", cat=LpBinary)



# Objective function: minimize the total cost
model += lpSum(x[i, day, shift] * (shift[1]-shift[0]) for i in employees for day in days for shift in weekly_shifts)
min_weekly_hours=10
max_weekly_hours=100
for i in employees:
    model += lpSum(x[i, day, shift]*(shift[1]-shift[0]) for day in days for shift in weekly_shifts) >= min_weekly_hours
    model += lpSum(x[i, day, shift] *(shift[1]-shift[0]) for day in days for shift in weekly_shifts) <= max_weekly_hours

# one shift per day for each employee 2

for i in employees:
    for day in days:
        model += lpSum(x[i, day, shift]  for shift in weekly_shifts) <= 1




# availability 
for i in employees:
    for day in days:
        start, end = availability[i][day]
        for shift in weekly_shifts:
            if shift[1] <= start or shift[0] < start or shift[0] >= end or  shift[1] > end or shift[0]< opening[day][0] or shift[1]> opening[day][1]:
                model += x[i, day, shift] == 0










# Constraint: Ensure at least one employee is present at each hour during the opening hours
for day in days:
    for hour in range(opening[day][0], opening[day][1]):
        model += lpSum(x[i, day, shift] for i in employees for shift in weekly_shifts if (hour >= shift[0] and hour < shift[1])) >= 1





model.solve()


if LpStatus[model.status] == 'Optimal':
    print("Optimal Solution Found.")
    for i in employees:
        for day in days:
            for shift in weekly_shifts:
                if x[i, day, shift].varValue == 1:
                    start_hour, end_hour = shift[0],shift[1]
                    print(f" {i} is assigned to Shift on {day} from {start_hour} to {end_hour}")
else:
    print("No feasible solution found.")