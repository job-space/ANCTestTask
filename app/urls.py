from django.urls import path
from .views import hierarchy_tree, employee_table, employee_table_data

urlpatterns = [
    path('hierarchy_tree', hierarchy_tree, name='hierarchy_tree'),
    path('employee_table', employee_table, name='employee_table'),
    path('employee_table_data', employee_table_data, name='employee_table_data'),

]
