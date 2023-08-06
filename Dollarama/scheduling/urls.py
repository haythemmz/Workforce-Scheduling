from django.urls import path
from . import views

urlpatterns = [
    # Define URL patterns for your views here
    # For example:
    path('', views.index, name='index'),  # This maps the root URL to the 'index' view
    path('add_employee_availability/', views.add_employee_availability, name='add_employee_availability'),
    path('add_store_hours/', views.add_store_hours, name='add_store_hours'),
    path('add_edit_employee/', views.add_edit_employee, name='add_edit_employee'),



]

