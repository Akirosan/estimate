from django.db import models
from django.shortcuts import render
from django.views.generic.edit import DeleteView, UpdateView
from .models import Calculate, Material, QuantityMaterial, QuantityWork, Work
from django.views.generic import ListView, CreateView
from django.urls import reverse
from django.urls import reverse_lazy

class DeleteMaterial(DeleteView):
    queryset = Material.objects.all()
    models = Material
    success_url = reverse_lazy('catalog_materials')
    template_name  = 'estimate/delete_materials.html'

class EditMaterial(UpdateView):
    queryset = Material.objects.all()
    models = Material
    fields = [ 'name', 'measurement_unit']
    template_name  = 'estimate/edit_materials.html'

    def get_success_url(self):
        return reverse('catalog_materials')
    

class AddMaterial(CreateView):
    queryset = Material.objects.all()
    models = Material
    fields = [ 'name', 'measurement_unit']
    template_name  = 'estimate/add_materials.html'

    def get_success_url(self):
        return reverse('catalog_materials')

class CatalogMaterialsView(ListView):
    queryset = Material.objects.all()
    context_object_name = 'materials'
    template_name = 'estimate/materials.html'

class CatalogWorksView(ListView):
    queryset = Work.objects.all()
    context_object_name = 'works'
    template_name = 'estimate/works.html'


class CalcListView(ListView):
    queryset = Calculate.objects.all()
    context_object_name = 'calculate'
    template_name = 'estimate/list.html'

def login(request):
    """Вывод второго шаблона"""
    estimate = Calculate.objects.all()
    return render(request, 'login.html', {'calculate': estimate})


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
