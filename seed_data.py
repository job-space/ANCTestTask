import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANCTestTask.settings')
django.setup()

from django_seed import Seed
from app.models import WorkerLevel1, WorkerLevel2, WorkerLevel3, WorkerLevel4, WorkerLevel5, WorkerLevel6, WorkerLevel7

seeder = Seed.seeder()

# Add one instance of WorkerLevel1
seeder.add_entity(WorkerLevel1, 1, {
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: seeder.faker.job(),
    'date_of_employment': lambda x: seeder.faker.date(),
    'email': lambda x: seeder.faker.email(),
    'table_name': 'WorkerLevel1',
})

# Start data generation
inserted_pks = seeder.execute()

# Saving WorkerLevel2 objects
boss_level_instance = WorkerLevel1.objects.first()

seeder.add_entity(WorkerLevel2, 5, {
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: seeder.faker.job(),
    'date_of_employment': lambda x: seeder.faker.date(),
    'email': lambda x: seeder.faker.email(),
    'boss_level': boss_level_instance,
    'table_name': 'WorkerLevel2',
})

inserted_pks = seeder.execute()


# Saving WorkerLevel3 objects
worker_level2_objects = WorkerLevel2.objects.all()

def random_boss(worker_level_objects):
    return seeder.faker.random_element(worker_level_objects)


seeder.add_entity(WorkerLevel3, 25, {
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: seeder.faker.job(),
    'date_of_employment': lambda x: seeder.faker.date(),
    'email': lambda x: seeder.faker.email(),
    'boss_level': lambda x: random_boss(worker_level2_objects),
    'table_name': 'WorkerLevel3',
})

inserted_pks = seeder.execute()


# Saving WorkerLevel4 objects
worker_level3_objects = WorkerLevel3.objects.all()

seeder.add_entity(WorkerLevel4, 125, {
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: seeder.faker.job(),
    'date_of_employment': lambda x: seeder.faker.date(),
    'email': lambda x: seeder.faker.email(),
    'boss_level': lambda x: random_boss(worker_level3_objects),
    'table_name': 'WorkerLevel4',
})

inserted_pks = seeder.execute()


# Saving WorkerLevel5 objects
worker_level4_objects = WorkerLevel4.objects.all()

seeder.add_entity(WorkerLevel5, 625, {
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: seeder.faker.job(),
    'date_of_employment': lambda x: seeder.faker.date(),
    'email': lambda x: seeder.faker.email(),
    'boss_level': lambda x: random_boss(worker_level4_objects),
    'table_name': 'WorkerLevel5',
})

inserted_pks = seeder.execute()


# Saving WorkerLevel6 objects
worker_level5_objects = WorkerLevel5.objects.all()

seeder.add_entity(WorkerLevel6, 3125, {
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: seeder.faker.job(),
    'date_of_employment': lambda x: seeder.faker.date(),
    'email': lambda x: seeder.faker.email(),
    'boss_level': lambda x: random_boss(worker_level5_objects),
    'table_name': 'WorkerLevel6',
})

inserted_pks = seeder.execute()


# Saving WorkerLevel7 objects
worker_level6_objects = WorkerLevel6.objects.all()

seeder.add_entity(WorkerLevel7, 46719, {
    'name': lambda x: seeder.faker.name(),
    'position': lambda x: seeder.faker.job(),
    'date_of_employment': lambda x: seeder.faker.date(),
    'email': lambda x: seeder.faker.email(),
    'boss_level': lambda x: random_boss(worker_level6_objects),
    'table_name': 'WorkerLevel7',
})

inserted_pks = seeder.execute()
