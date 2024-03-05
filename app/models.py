from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    date_of_employment = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=100)

    class Meta:
        abstract = True


class WorkerLevel1(BaseModel):
    table_name = models.CharField(max_length=100, default='WorkerLevel1')

    def __str__(self):
        return self.name


class WorkerLevel2(BaseModel):
    table_name = models.CharField(max_length=100, default='WorkerLevel2')
    boss_level = models.ForeignKey(WorkerLevel1, on_delete=models.SET_NULL, related_name='worker_level_2', blank=True, null=True)

    def __str__(self):
        return self.name


class WorkerLevel3(BaseModel):
    table_name = models.CharField(max_length=100, default='WorkerLevel3')
    boss_level = models.ForeignKey(WorkerLevel2, on_delete=models.SET_NULL, related_name='worker_level_3', blank=True, null=True)

    def __str__(self):
        return self.name


class WorkerLevel4(BaseModel):
    table_name = models.CharField(max_length=100, default='WorkerLevel4')
    boss_level = models.ForeignKey(WorkerLevel3, on_delete=models.SET_NULL, related_name='worker_level_4', blank=True, null=True)

    def __str__(self):
        return self.name


class WorkerLevel5(BaseModel):
    table_name = models.CharField(max_length=100, default='WorkerLevel5')
    boss_level = models.ForeignKey(WorkerLevel4, on_delete=models.SET_NULL, related_name='worker_level_5', blank=True, null=True)

    def __str__(self):
        return self.name


class WorkerLevel6(BaseModel):
    table_name = models.CharField(max_length=100, default='WorkerLevel6')
    boss_level = models.ForeignKey(WorkerLevel5, on_delete=models.SET_NULL, related_name='worker_level_6', blank=True, null=True)

    def __str__(self):
        return self.name


class WorkerLevel7(BaseModel):
    table_name = models.CharField(max_length=100, default='WorkerLevel7')
    boss_level = models.ForeignKey(WorkerLevel6, on_delete=models.SET_NULL, related_name='worker_level_7', blank=True, null=True)

    def __str__(self):
        return self.name
