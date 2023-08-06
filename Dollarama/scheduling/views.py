from django.shortcuts import render, redirect
from .forms import EmployeeForm,StoreHoursForm
from .models import Employee, EmployeeAvailability,StoreHours,DAY_CHOICES
from .forms import EmployeeForm, EmployeeAvailabilityForm




# views.py

# views.py


def add_edit_employee(request, employee_id=None):
    employee = None
    employee_availability = [None] * len(DAY_CHOICES)
    if employee_id:
        employee = Employee.objects.get(pk=employee_id)
        employee_availability_qs = EmployeeAvailability.objects.filter(employee=employee)
        for availability in employee_availability_qs:
            day_index = next((i for i, day_choice in enumerate(DAY_CHOICES) if day_choice[0] == availability.day), None)
            if day_index is not None:
                employee_availability[day_index] = availability

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        availability_forms = [EmployeeAvailabilityForm(prefix=str(day), data=request.POST, instance=availability)
                              if availability else EmployeeAvailabilityForm(prefix=str(day), data=request.POST)
                              for day, availability in zip(DAY_CHOICES, employee_availability)]
        if form.is_valid() and all(formset.is_valid() for formset in availability_forms):
            employee = form.save()
            for availability_form in availability_forms:
                if availability_form.cleaned_data:
                    availability = availability_form.save(commit=False)
                    availability.employee = employee
                    availability.save()
            return redirect('index')
    else:
        form = EmployeeForm(instance=employee)
        availability_forms = [EmployeeAvailabilityForm(prefix=str(day), instance=availability)
                              if availability else EmployeeAvailabilityForm(prefix=str(day))
                              for day, availability in zip(DAY_CHOICES, employee_availability)]

    return render(request, 'add_edit_employee.html', {
        'form': form,
        'availability_forms': availability_forms,
    })


# views.py

def add_store_hours(request):
    if request.method == 'POST':
        form = StoreHoursForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            # Remove old store hours for the chosen day
            StoreHours.objects.filter(day=day).delete()
            form.save()
            return redirect('add_store_hours')
    else:
        form = StoreHoursForm()

    store_hours = StoreHours.objects.all()  # Fetch all the stored store hours

    return render(request, 'add_store_hours.html', {'form': form, 'store_hours': store_hours})





def add_employee_availability(request):
    if request.method == 'POST':
        form = EmployeeAvailabilityForm(request.POST)
        if form.is_valid():
            employee = Employee.objects.get(pk=request.POST['employee'])
            day = request.POST['day']
            start_hour = int(request.POST['start_hour'])
            end_hour = int(request.POST['end_hour'])
            EmployeeAvailability.objects.create(employee=employee, day=day, start_hour=start_hour, end_hour=end_hour)
            return redirect('index')

    else:
        form = EmployeeAvailabilityForm()

    return render(request, 'add_employee_availability.html', {'form': form})


def index(request):
    # Add your logic here to handle the request
    # For example, you can fetch data from the database and pass it to the template
    data = {
        'message': 'Hello, this is the index page!',
    }
    return render(request, 'index.html', data)


