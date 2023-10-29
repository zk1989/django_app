from django import forms

from .models import MealType

class MealTypeForm(forms.ModelForm):
    class Meta:
        model = MealType
        fields = ['text']
        labels = {'text': ''}
