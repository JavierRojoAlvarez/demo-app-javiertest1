from django.db import models
from buildings.models import Building


class CashflowCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cost Types'


class Cashflow(models.Model):
    start = models.DateField()
    end = models.DateField()
    category = models.ForeignKey(
        CashflowCategory, on_delete=models.CASCADE, default=''
    )
    building = models.ForeignKey(
        Building, on_delete=models.CASCADE, default=''
    )
    option = models.IntegerField()
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0)

    def __str__(self):
        return f'{self.category}:{self.start}'
