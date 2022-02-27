from re import M
from django import forms

class AddWorkForm(forms.Form):
    name = forms.CharField(max_length=50, label="", widget=forms.TextInput(attrs={'placeholder': 'наименование'}))
    measurement_unit = forms.CharField(max_length=10, label="", widget=forms.TextInput(attrs={'placeholder': 'еденица измерения'}))
    price = forms.FloatField(label="", widget=forms.TextInput(attrs={'placeholder': 'цена'}))


class SearchMaterialForm(forms.Form):
    search_query = forms.CharField(max_length=50, help_text="Название материала")