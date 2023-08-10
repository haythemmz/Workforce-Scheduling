from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm,StoreHoursForm
from .models import Employee,StoreHours,DAY_CHOICES
import logging

logger = logging.getLogger(__name__)

def index(request):
    employees = Employee.objects.all()
    return render(request, 'index.html', {'employees': employees})

def add_edit_employee(request, employee_id=None):
    employee = None

    if employee_id:
        employee = get_object_or_404(Employee, pk=employee_id)

    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST, instance=employee)
        logger.info("POST data: %s", request.POST)
        employee_form = EmployeeForm(request.POST, instance=employee)
        if employee_form.is_valid():
           
            employee = employee_form.save(commit=False)
            # Save the employee's availability manually
            employee.start_monday = request.POST.get('start_monday')
            employee.end_monday = request.POST.get('end_monday')
            employee.start_tuesday = request.POST.get('start_tuesday')
            employee.end_tuesday = request.POST.get('end_tuesday')
            employee.start_wednesday = request.POST.get('start_wednesday')
            employee.end_wednesday = request.POST.get('end_wednesday')
            employee.start_thursday = request.POST.get('start_thursday')
            employee.end_thursday = request.POST.get('end_thursday')
            employee.start_friday = request.POST.get('start_friday')
            employee.end_friday = request.POST.get('end_friday')
            employee.start_saturday = request.POST.get('start_saturday')
            employee.end_saturday = request.POST.get('end_saturday')
            employee.start_sunday = request.POST.get('start_sunday')
            employee.end_sunday = request.POST.get('end_sunday')
            employee.save()
            
            # Redirect to the employee detail view with the newly added/edited employee's ID
            return redirect('employee_detail', employee_id=employee.id)
        else:
            logger.info("Form data is valid")
    else:
        employee_form = EmployeeForm(instance=employee)

    return render(request, 'add_edit_employee.html', {
        'employee_form': employee_form,
    })

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'employee_detail.html', {'employee': employee})

def add_store_hours(request):
    if request.method == 'POST':
        form = StoreHoursForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            StoreHours.objects.filter(day=day).delete()
            form.save()
            return redirect('add_store_hours')
    else:
        form = StoreHoursForm()

    store_hours = StoreHours.objects.all()  # Fetch all the stored store hours

    return render(request, 'add_store_hours.html', {'form': form, 'store_hours': store_hours})











