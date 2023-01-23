from django.db import models


class AccountType(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Account Types'


class Hierarchy1(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Hierarchy2(models.Model):
    hierarchy1 = models.ForeignKey(
        Hierarchy1, on_delete=models.CASCADE, default=''
    )
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Hierarchy3(models.Model):
    hierarchy2 = models.ForeignKey(
        Hierarchy2, on_delete=models.CASCADE, default=''
    )
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Hierarchy4(models.Model):
    hierarchy3 = models.ForeignKey(
        Hierarchy3, on_delete=models.CASCADE, default=''
    )
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name


class Account(models.Model):
    number = models.IntegerField()
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    hierarchy4 = models.ForeignKey(Hierarchy4, on_delete=models.CASCADE)
    description = models.CharField(max_length=50, default='')
    is_live = models.BooleanField('Live', default=True)

    class Meta:
        ordering = ('description',)

    def __str__(self):
        return self.description
