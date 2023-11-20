from django import forms
from .models import AppModel

class AppForm(forms.ModelForm):
    class Meta:
        model = AppModel
        param_key = forms.CharField(max_length=255)
        param_value = forms.CharField(max_length=255)
        request_body = forms.CharField(max_length=250,required=False)
        header_key = forms.CharField(max_length=255)
        header_value = forms.CharField(max_length=255)
        basic_username = forms.CharField(max_length=255,required=False)
        basic_password = forms.CharField(max_length=250,required=False)
        auth_type = forms.CharField(max_length=100,required=False)
        fields = ['url', 'method']