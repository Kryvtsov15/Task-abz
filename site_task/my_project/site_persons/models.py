from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField



class Human(MPTTModel):
    full_name = models.CharField(max_length=150, default="", verbose_name='ФИО')
    """position = models.ForeignKey(Position, null=True, on_delete=models.SET_NULL, verbose_name='Должность')"""
    position = models.CharField(max_length= 150, verbose_name='Должность')
    employment_date = models.DateField(auto_now=False, verbose_name='Дата прийома на работу')
    salary = models.IntegerField(verbose_name='Зарплата')
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="children", verbose_name='Начальник')

    search_index = VectorField()



    search_manager = SearchManager(
        fields=('full_name', 'position'),
        config='pg_catalog.russian',
        search_field='search_index',
        auto_update_search_field=True
    )


    class MPTTMeta:
        unique_together = (('full_name', 'parent'),)

    def __str__(self):
        return self.full_name