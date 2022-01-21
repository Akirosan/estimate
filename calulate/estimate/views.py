from re import M
from unicodedata import name
from django.db import models
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from .models import Calculate, Material, QuantityMaterial, QuantityWork, Work
from django.views.generic import ListView, CreateView
from django.urls import reverse
from django.urls import reverse_lazy

class DeleteMaterial(DeleteView):
    """Удаляет материал из каталога материалов"""
    queryset = Material.objects.all()
    models = Material
    success_url = reverse_lazy('catalog_materials')
    template_name  = 'estimate/delete_materials.html'

class EditMaterial(UpdateView):
    """Редактирует материал в каталоге материалов"""
    queryset = Material.objects.all()
    models = Material
    fields = [ 'name', 'measurement_unit', 'price']
    template_name  = 'estimate/edit_materials.html'

    def get_success_url(self):
        return reverse('catalog_materials')
    

class AddMaterial(CreateView):
    """Создает материал в каталог материалов"""
    queryset = Material.objects.all()
    models = Material
    fields = [ 'name', 'measurement_unit', 'price']
    template_name  = 'estimate/add_materials.html'

    def get_success_url(self):
        return reverse('catalog_materials')


class CatalogMaterialsView(ListView):
    """Выводит материалы из каталога материалов"""
    queryset = Material.objects.all()
    context_object_name = 'materials'
    template_name = 'estimate/materials.html'


class CatalogWorksView(ListView):
    """Выводит список видов работ из каталога видов работ"""
    queryset = Work.objects.all()
    context_object_name = 'works'
    template_name = 'estimate/works.html'


class CalcListView(ListView):
    """Выводит список расчетов"""
    queryset = Calculate.objects.all()
    context_object_name = 'calculate'
    template_name = 'estimate/list.html'

def login(request): # Переместить в модуль user
    """Вывод шаблона авторизации"""
    return render(request, 'login.html')


def view_detail(request, *args, **kwargs):
    """Вывод деталей сметы с материалом и работами"""
    calculate = Calculate.objects.get(slug=kwargs['slug'])
    materials = QuantityMaterial.objects.filter(calculate=calculate)
    works = QuantityWork.objects.filter(calculate=calculate)
    # import ipdb; ipdb.set_trace()

    return render(
        request, 'estimate/detail.html', {
            'calculate': calculate,
            'materials': materials,
            'works': works,
            'total': total_price(materials, works),
        }
    )

def total_price(materials, works):
    """Считаем ИТОГО по материалам и работам"""
    total_work_price = 0
    for work in works:
        total_work_price+=work.amount

    total_material_price = 0
    for material in materials:
        total_material_price+=material.amount

    return {'material': total_material_price, 'work': total_work_price}

class AddCalc(CreateView):
    """Создает новую смету"""
    queryset = Calculate.objects.all()
    models = Calculate
    fields = ['name', 'slug','text','difficulty_factor','fuel_price','tupe_calc', 'author']
    template_name  = 'estimate/detail.html'

    def get_success_url(self):
        return reverse('view_estimate_detail')


def delete_material_from_calc(request, *args, **kwargs):
    """Удаляет материал из сметы"""
    pass
    # queryset = Material.objects.all()
    # models = Material
    # success_url = reverse_lazy('catalog_materials')
    # template_name  = 'estimate/delete_materials.html'



class SearchMaterialListView(ListView):  # 
    """Поиск материалов для добавления в смету"""
    # context_object_name = 'materials'
    template_name = 'estimate/search.html'
    model = Material

    def get_queryset(self):  # Ищем материалы соответствующие запросу из формы
        query = self.request.GET.get('search_query')
        # import ipdb; ipdb.set_trace()
        materials = Material.objects.filter(name__icontains=query)
        # import ipdb; ipdb.set_trace()
        return materials
    
    def get_context_data(self, **kwargs):  # Добавляет в контекст шаблона ID сметы в которую нужно добавить материал
        context = super().get_context_data(**kwargs)
        # import ipdb; ipdb.set_trace()
        context['calc_id'] = 'ID сметы в контексте для возврата к ней при добавлении материала def get_context_data'
        return context