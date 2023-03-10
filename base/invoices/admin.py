from django.contrib import admin
from django.apps import apps
from import_export.admin import ImportExportModelAdmin
app_dict = apps.all_models['invoices']
model_list = [v for v in app_dict.values()]


@admin.register(*model_list)
class ViewAdmin(ImportExportModelAdmin):
    pass
