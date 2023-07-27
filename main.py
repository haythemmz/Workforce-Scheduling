from pulp import *

# Create a LP problem object
prob = LpProblem("WorkforceScheduling", LpMinimize)

# Define the employee availability
availability = {
    'Employee1': {
        'Monday': [1, 1, 1],
        'Tuesday': [0, 1, 1],
        'Wednesday': [1, 0, 1]
    },
    'Employee2': {
        'Monday': [1, 0, 1],
        'Tuesday': [1, 1, 1],
        'Wednesday': [1, 1, 0]
    }
}

# Define the minimum and maximum hours per week and per shift
min_hours_per_week = 15
max_hours_per_week = 30
min_hours_per_shift = 3
max_hours_per_shift = 8

# Define the cost per hour
cost_per_hour = 10

# Create the decision variables
employees = list(availability.keys())
days = list(availability[employees[0]].keys())
time_slots = range(len(availability[employees[0]][days[0]]))

x = LpVariable.dicts("Assign", (employees, days, time_slots), 0, 1, LpBinary)

# Define the objective function: minimize total cost
prob += lpSum(x[i][d][t] for i in employees for d in days for t in time_slots) * cost_per_hour, "Total_Cost"

# Constraints

# Minimum and maximum hours per week
for i in employees:
    prob += lpSum(x[i][d][t] for d in days for t in time_slots) >= min_hours_per_week
    prob += lpSum(x[i][d][t] for d in days for t in time_slots) <= max_hours_per_week

# Minimum and maximum hours per shift
for d in days:
    for t in time_slots:
        prob += lpSum(x[i][d][t] for i in employees) >= min_hours_per_shift
        prob += lpSum(x[i][d][t] for i in employees) <= max_hours_per_shift

# Employee availability
for i in employees:
    for d in days:
        for t in time_slots:
            prob += x[i][d][t] <= availability[i][d][t]

# Coverage requirement
for d in days:
    for t in time_slots:
        prob += lpSum(x[i][d][t] for i in employees) >= 1

# Solve the problem
prob.solve()

# Print the status of the problem
print("Status:", LpStatus[prob.status])

# Print the optimal schedule
for i in employees:
    for d in days:
        for t in time_slots:
            if x[i][d][t].value() == 1:
                print(f"Employee {i} works on {d} during time slot {t}.")

# Print the total cost
print("Total Cost:", value(prob.objective))
