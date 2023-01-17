from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.name


class Building(models.Model):
    epims_id = models.CharField('ePIMS ID', max_length=50)
    name = models.CharField('Name', max_length=50)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, default='')
    nia = models.DecimalField(
        'NIA', decimal_places=2, max_digits=20, default=0
    )
    ftes_capacity = models.DecimalField(
        'FTEs Capacity', decimal_places=2, max_digits=20, default=0
    )
    image = models.ImageField(default='images/default.png', upload_to='images')
    cost_centre = models.CharField('Cost Centre', max_length=50, default='')

    def __str__(self):
        return self.name
