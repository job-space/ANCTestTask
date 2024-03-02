from django.shortcuts import render
from .models import WorkerLevel1, WorkerLevel2, WorkerLevel3, WorkerLevel4, WorkerLevel5, WorkerLevel6, WorkerLevel7
from django.http import JsonResponse
from django.db.models import OuterRef, Subquery
from django.db.models import Q


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
