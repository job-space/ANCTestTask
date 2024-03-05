from django.http import JsonResponse,HttpResponse
from django.db.models import OuterRef, Subquery, Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.apps import apps
from django.views.decorators.http import require_POST, require_http_methods
from django.core.serializers import serialize
import json

from .models import WorkerLevel1, WorkerLevel2, WorkerLevel3, WorkerLevel4, WorkerLevel5, WorkerLevel6, WorkerLevel7


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
            boss_worker.table_name = worker.table_name
            boss_worker.save()
    finally:
        worker.delete()

    return HttpResponse('Success')


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


def hierarchy_tree(request):
    worker = WorkerLevel1.objects.get()
    context = {
        'worker': worker,
    }

    return render(request, 'hierarchy_tree.html', context=context)


def employee_table_data(request):
    sort_param = request.GET.get('sort', 'name')
    search_param = request.GET.get('query', '')

    # Obtaining data on employees and sorting by the specified field
    workers_level1 = WorkerLevel1.objects.values('name', 'position', 'date_of_employment', 'email')
    workers_level2 = WorkerLevel2.objects.values('name', 'position', 'date_of_employment', 'email', 'boss_level_1__name')
    workers_level3 = WorkerLevel3.objects.values('name', 'position', 'date_of_employment', 'email', 'boss_level_2__name')
    workers_level4 = WorkerLevel4.objects.values('name', 'position', 'date_of_employment', 'email', 'boss_level_3__name')
    workers_level5 = WorkerLevel5.objects.values('name', 'position', 'date_of_employment', 'email', 'boss_level_4__name')
    workers_level6 = WorkerLevel6.objects.values('name', 'position', 'date_of_employment', 'email', 'boss_level_5__name')
    workers_level7 = WorkerLevel7.objects.values('name', 'position', 'date_of_employment', 'email', 'boss_level_6__name')

    # create an additional instance for workers_level1 to use union
    boss_level = WorkerLevel7.objects.filter(boss_level_6=OuterRef('pk')).values('name')[:1]
    workers_level1 = workers_level1.annotate(boss_level=Subquery(boss_level))

    if search_param:
        workers_level2 = workers_level2.filter(
            Q(name__icontains=search_param) |
            Q(position__icontains=search_param) |
            Q(email__icontains=search_param) |
            Q(date_of_employment__icontains=search_param) |
            Q(boss_level_1__name__icontains=search_param)
        )

    workers = workers_level1.union(workers_level2, workers_level3, workers_level4, workers_level5, workers_level6, workers_level7).order_by(sort_param)

    # delete the additional instance
    for worker in workers:
        if worker == workers_level1[0]:
            worker.pop('boss_level', None)

        # Create a response in JSON format
    data = {
        'workers': list(workers),
        'current_sort': sort_param,
    }

    # Returning a response in JSON format
    return JsonResponse(data)


def employee_table(request):
    return render(request, 'employee_table.html')
