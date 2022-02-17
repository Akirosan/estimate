from re import M
from django import forms

class AddWorkForm(forms.Form):
    name = forms.CharField(max_length=50, help_text="Название работы")
    measurement_unit = forms.CharField(max_length=10, help_text="ед.изм")
    price = forms.FloatField(help_text="цена")


class SearchMaterialForm(forms.Form):
    search_query = forms.CharField(max_length=50, help_text="Название материала")