from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.apps import apps
from django.views.decorators.http import require_POST, require_http_methods
from django.core.serializers import serialize
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

import json
from .models import WorkerLevel1, WorkerLevel2, WorkerLevel3, WorkerLevel4, WorkerLevel5, WorkerLevel6, WorkerLevel7


@login_required
@require_http_methods(["GET", "POST"])
def get_bosses_based_on_level(request):
    selected_level_id = request.POST.get('selectedLevelId')
    if selected_level_id:
        if int(selected_level_id) == 1:
            bosses_data = []
        else:
            model_boss = apps.get_model(app_label='app', model_name=f'WorkerLevel{int(selected_level_id[-1]) - 1}')
            bosses = model_boss.objects.all()
            serialized_bosses = serialize('json', bosses)
            bosses_data = json.loads(serialized_bosses)
    else:
        bosses_data = []
    return JsonResponse({'bosses': list(bosses_data)})


def get_boss_levels(request):

    boss_levels = [
        {'id': 1, 'name': 'WorkerLevel1'},
        {'id': 2, 'name': 'WorkerLevel2'},
        {'id': 3, 'name': 'WorkerLevel3'},
        {'id': 4, 'name': 'WorkerLevel4'},
        {'id': 5, 'name': 'WorkerLevel5'},
        {'id': 6, 'name': 'WorkerLevel6'},
        {'id': 7, 'name': 'WorkerLevel7'},
    ]

    return JsonResponse({'bossLevels': boss_levels})


@login_required
def add_employee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        position = request.POST.get('position')
        date = request.POST.get('date')
        email = request.POST.get('email')
        level_worker = request.POST.get('level_worker')
        boss = request.POST.get('boss')

        model_worker = apps.get_model(app_label='app', model_name=f'WorkerLevel{level_worker}')

        try:
            if model_worker.boss_level:
                model_boss = apps.get_model(app_label='app', model_name=f'WorkerLevel{int(level_worker[-1]) - 1}')
                boss = model_boss.objects.get(id=int(boss))
                new_worker = model_worker(name=name, position=position, date_of_employment=date, email=email,
                                          boss_level=boss)
                new_worker.save()
        except:
            boss = model_worker.objects.first()
            model_subordinates = apps.get_model(app_label='app', model_name=f'WorkerLevel{int(level_worker[-1]) + 1}')
            new_subordinates = model_subordinates(name=boss.name, position=boss.position,
                                                  date_of_employment=boss.date_of_employment,
                                                  email=boss.email, boss_level=boss)
            new_subordinates.save()

            boss.name = name
            boss.position = position
            boss.date_of_employment = date
            boss.email = email
            boss.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required
@require_POST
def delete_employee(request):
    employee_id = request.POST.get('employee_id')
    worker_level = request.POST.get('table_name')

    model = apps.get_model(app_label='app', model_name=worker_level)
    worker = model.objects.get(id=employee_id)

    boss_worker = None

    if worker_level == 'WorkerLevel1':
        boss_worker = model.objects.first()
        worker_level = f'WorkerLevel{int(worker_level[-1]) + 1}'
        worker = apps.get_model(app_label='app', model_name=worker_level).objects.first()

    workers_level = apps.get_model(app_label='app', model_name=worker_level).objects.exclude(name=worker.name)

    try:
        model_subordinates = apps.get_model(app_label='app', model_name=f'WorkerLevel{int(worker_level[-1]) + 1}')
        workers_subordinates = model_subordinates.objects.filter(boss_level=worker.id)

        num_employees = len(workers_subordinates)
        num_bosses = len(workers_level)

        for i, boss in enumerate(workers_level):
            num_assignments = num_employees // num_bosses
            num_employees -= num_assignments

            for j in range(num_assignments):
                subordinate = workers_subordinates.first()

                if subordinate:
                    print(f"Boss: {boss.name}, Assigned Employees: {subordinate.name}")
                    subordinate.boss_level = boss
                    subordinate.save()
                    workers_subordinates = workers_subordinates.exclude(id=subordinate.id)

        for i, boss in enumerate(workers_level):
            if num_employees > 0:
                subordinate = workers_subordinates.first()
                if subordinate:
                    subordinate.boss_level = boss
                    subordinate.save()
                    workers_subordinates = workers_subordinates.exclude(id=subordinate.id)
                    num_employees -= 1
    except LookupError:
        worker.delete()
        return HttpResponse('Success')
    except Exception as e:
        print(f"Error: {e}")

    try:
        if boss_worker:
            boss_worker.name = worker.name
            boss_worker.position = worker.position
            boss_worker.date_of_employment = worker.date_of_employment
            boss_worker.email = worker.email
            boss_worker.save()
    finally:
        worker.delete()

    return HttpResponse('Success')


@login_required
@require_POST
def save_edited_employee(request):
    employee_id = request.POST.get('employee_id')
    name = request.POST.get('name')
    position = request.POST.get('position')
    table_name = request.POST.get('table_name')

    date = request.POST.get('date')
    email = request.POST.get('email')
    boss_level = request.POST.get('bossLevel')

    model = apps.get_model(app_label='app', model_name=table_name)
    employee = model.objects.get(id=employee_id)

    employee.name = name
    employee.position = position
    employee.date = date
    employee.email = email

    try:
        if boss_level:
            model_boss = apps.get_model(app_label='app', model_name=employee.boss_level.table_name)
            employee.boss_level = model_boss.objects.get(id=boss_level)

    finally:
        employee.save()

    return HttpResponse('Success')


def get_employee_data(request):
    employee_id = request.POST.get('employee_id')
    worker_level = request.POST.get('workerLevel')

    model = apps.get_model(app_label='app', model_name=worker_level)
    employee = get_object_or_404(model, id=employee_id)
    employee_dict = model.objects.filter(id=employee_id).values().first()

    try:

        boss = employee.boss_level.name
    except:
        boss = False
    bosses = []
    if boss != False:
        model = apps.get_model(app_label='app', model_name=employee.boss_level.table_name)
        bosses = list(model.objects.all().values())

    bosses = sorted(bosses, key=lambda x: x['id'] == employee.boss_level.id, reverse=True)
    data = {
        'name': employee_dict['name'],
        'position': employee_dict['position'],
        'email': employee_dict['email'],
        'date_of_employment': employee_dict['date_of_employment'],
        'boss_level': boss,
        'bosses': bosses,
    }
    return JsonResponse(data)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm
    success_url = reverse_lazy('employee_table')

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        login(self.request, form.get_user())
        return super().form_valid(form)


@csrf_exempt
def get_subordinates(request):
    employee_id = request.POST.get('post_id')
    worker_level = request.POST.get('level')
    showed = request.POST.get('showed')

    model = apps.get_model(app_label='app', model_name=worker_level)  # worker level
    worker = model.objects.get(id=employee_id)  # worker name

    if worker_level == 'WorkerLevel1':  # The first download
        subordinates = list(
            getattr(worker, f"worker_level_{int(worker_level[-1]) + 1}").values('id', 'name', 'position', 'table_name'))
    elif showed:
        current_model = apps.get_model(app_label='app', model_name=worker_level)
        subordinates = list(
            current_model.objects.values('id', 'name', 'position', 'table_name'))
    elif worker_level in ['WorkerLevel2']:
        subordinates = get_subordinates_recursive(worker, int(worker_level[-1]) + 1)

    else:
        subordinates = []

    return JsonResponse({'subordinates': subordinates})


def get_subordinates_recursive(worker, next_level):
    subordinates = []

    if next_level > 7:  # Test to the maximum level
        return subordinates

    subordinate_manager = f'worker_level_{next_level}'

    for subordinate in getattr(worker, subordinate_manager).all():
        subordinate_data = {
            'id': subordinate.id,
            'name': subordinate.name,
            'position': subordinate.position,
            'table_name': subordinate.table_name,
            'subordinates': get_subordinates_recursive(subordinate, next_level + 1),
        }
        subordinates.append(subordinate_data)

    return subordinates


def hierarchy_tree(request):
    worker = WorkerLevel1.objects.get()
    context = {
        'worker': worker,
    }

    return render(request, 'hierarchy_tree.html', context=context)


def employee_table_data(request):
    sort_param = request.GET.get('sort', 'name')
    search_param = request.GET.get('query', '')

    # Retrieve employee data and sort by a specified field
    workers_level1 = WorkerLevel1.objects.values('id', 'name', 'position', 'date_of_employment', 'email', 'table_name',)
    workers_level2 = WorkerLevel2.objects.values('id', 'name', 'position', 'date_of_employment', 'email', 'table_name', 'boss_level__name')
    workers_level3 = WorkerLevel3.objects.values('id', 'name', 'position', 'date_of_employment', 'email', 'table_name', 'boss_level__name')
    workers_level4 = WorkerLevel4.objects.values('id', 'name', 'position', 'date_of_employment', 'email', 'table_name', 'boss_level__name')
    workers_level5 = WorkerLevel5.objects.values('id', 'name', 'position', 'date_of_employment', 'email', 'table_name', 'boss_level__name')
    workers_level6 = WorkerLevel6.objects.values('id', 'name', 'position', 'date_of_employment', 'email', 'table_name', 'boss_level__name')
    workers_level7 = WorkerLevel7.objects.values('id', 'name', 'position', 'date_of_employment', 'email', 'table_name', 'boss_level__name')

    workers_level1_list = list(workers_level1)
    workers_level2_list = list(workers_level2)
    workers_level3_list = list(workers_level3)
    workers_level4_list = list(workers_level4)
    workers_level5_list = list(workers_level5)
    workers_level6_list = list(workers_level6)
    workers_level7_list = list(workers_level7)

    # Combine lists into one common list
    all_workers = (
            workers_level1_list +
            workers_level2_list +
            workers_level3_list +
            workers_level4_list +
            workers_level5_list +
            workers_level6_list +
            workers_level7_list
    )

    # Manually sort the list by the specified parameter
    all_workers.sort(key=lambda x: x.get(sort_param, ''))

    for worker in all_workers:
        if 'boss_level__name' in worker:
            worker['boss_level'] = worker.pop('boss_level__name')

    # Filter if the search parameter is passed
    if search_param:
        all_workers = filter(
            lambda worker: (
                    search_param.lower() in worker.get('name', '').lower() or
                    search_param.lower() in worker.get('position', '').lower() or
                    search_param.lower() in worker.get('email', '').lower() or
                    search_param.lower() in str(worker.get('date_of_employment', '')).lower() or
                    (worker.get('boss_level') and search_param.lower() in worker['boss_level'].lower())
            ),
            all_workers
        )

    data = {
        'workers': list(all_workers),
        'current_sort': sort_param,
    }

    return JsonResponse(data)


def employee_table(request):
    return render(request, 'employee_table.html')


def logout_user(request):
    logout(request)
    return redirect('login')
