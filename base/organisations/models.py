from django.db import models


class OrganisationType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Organisation Types'


class Organisation(models.Model):
    name = models.CharField(max_length=50)
    organisation_type = models.ForeignKey(
        OrganisationType, on_delete=models.CASCADE, null=True, blank=True
    )
    reference = models.IntegerField()
    sort_code = models.IntegerField()
    account_number = models.IntegerField()
    postcode = models.CharField(max_length=50, default='')
    address = models.TextField(max_length=200, default='')

    def __str__(self):
        return self.name
