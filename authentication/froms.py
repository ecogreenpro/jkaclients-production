from django import forms
from django.forms import TextInput, Select, FileInput, Textarea, HiddenInput, DateInput

from authentication.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company_name', 'date_of_birth', 'address', 'phone', 'gender', 'district', 'country']
        widgets = {
            'company_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Company'}),
            'date_of_birth': DateInput(
                attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}),
            'gender': Select(attrs={'class': 'form-select form-control', 'placeholder': 'Gender'}),
            'address': TextInput(
                attrs={'class': 'form-control', 'placeholder': 'House No, Flat No, Road No, Location'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),

            'district': TextInput(attrs={'class': 'form-control', 'placeholder': 'Division'}),
            'country': Select(attrs={'class': 'form-select form-control', 'placeholder': 'Country'}),
        }
