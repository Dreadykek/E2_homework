from django import forms
from app.models import Massage


class MassageForm(forms.ModelForm):
    class Meta:
        model = Massage
        fields = ['text', 'from_email', 'to_email']