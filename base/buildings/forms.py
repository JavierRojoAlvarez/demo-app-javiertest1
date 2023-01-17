from django import forms
from buildings.models import Building


reg_attrs = {'class': 'form-control form-control-md rounded'}
check_attrs = {
    'class': 'form-control form-control-sm', 'style': 'width: 1.5rem;'
}
date_attrs = {
    'class': 'form-control form-control-md rounded date-input', 'name': 'date'
}
req_attrs = {'required': 'required'}


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        widgets = {
            'epims_id': forms.TextInput(attrs=reg_attrs),
            'name': forms.TextInput(attrs=reg_attrs),
            'region': forms.Select(attrs=reg_attrs),
            'nia': forms.NumberInput(attrs=reg_attrs),
            'ftes_capacity': forms.NumberInput(attrs=reg_attrs),
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
        fields = list(widgets.keys())
