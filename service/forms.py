from django import forms
from django.forms import TextInput, Select

from service.models import MyService


class FileUploadForm(forms.Form):
    file = forms.FileField()


class ServiceUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ServiceUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user'].initial = self.request.user

    class Meta:
        model = MyService
        fields = ['user', 'service', 'my_service_description']
        widgets = {
            'user': forms.HiddenInput(),
            'service': Select(attrs={'class': 'form-select form-control', 'placeholder': 'Service'}),
            'my_service_description': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Notes'}),
        }
