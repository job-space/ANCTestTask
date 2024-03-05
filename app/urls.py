from .views import hierarchy_tree, employee_table, employee_table_data, CustomLoginView, \
    get_employee_data, save_edited_employee, delete_employee, add_employee, get_boss_levels, get_bosses_based_on_level
from django.urls import path


urlpatterns = [
    path('hierarchy_tree', hierarchy_tree, name='hierarchy_tree'),
    path('employee_table', employee_table, name='employee_table'),
    path('employee_table_data', employee_table_data, name='employee_table_data'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('get_employee_data', get_employee_data, name='get_employee_data'),
    path('save_edited_employee', save_edited_employee, name='save_edited_employee'),
    path('delete_employee', delete_employee, name='delete_employee'),
    path('add_employee', add_employee, name='add_employee'),
    path('get_boss_levels', get_boss_levels, name='get_boss_levels'),
    path('get_bosses_based_on_level', get_bosses_based_on_level, name='get_bosses_based_on_level'),
]
