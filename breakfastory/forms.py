from django import forms

from .models import MealType, Entry

class MealTypeForm(forms.ModelForm):
    class Meta:
        model = MealType
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
