from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import DeleteView, UpdateView
from .models import Calculate, Material, QuantityMaterial, QuantityWork, Work
from django.views.generic import ListView, CreateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect


class DeleteMaterial(DeleteView):
    """Удаляет материал из каталога материалов"""
    queryset = Material.objects.all()
    models = Material
    success_url = reverse_lazy('catalog_materials')
    template_name = 'estimate/delete_materials.html'


class EditMaterial(UpdateView):
    """Редактирует материал в каталоге материалов"""
    queryset = Material.objects.all()
    models = Material
    fields = ['name', 'measurement_unit', 'price']
    template_name = 'estimate/edit_materials.html'

    def get_success_url(self):
        return reverse('catalog_materials')
    

class AddMaterial(CreateView):
    """Создает материал в каталог материалов"""
    queryset = Material.objects.all()
    models = Material
    fields = ['name', 'measurement_unit', 'price']
    template_name = 'estimate/add_materials.html'

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


def login(request):  # Переместить в модуль user
    """Вывод шаблона авторизации"""
    return render(request, 'login.html')


def view_detail(request, *args, **kwargs):
    """Вывод деталей сметы с материалом и работами"""
    calculate = Calculate.objects.get(slug=kwargs['slug'])
    materials = QuantityMaterial.objects.filter(calculate=calculate)
    works = QuantityWork.objects.filter(calculate=calculate)
    return render(
        request, 'estimate/detail.html', {
            'calculate': calculate,
            'materials': materials,
            'works': works,
            'total': total_price(materials, works),
        }
    )


def edit_mat_in_calc(request, *args, **kwargs):
    """Редактирует материалы на странице сметы"""
    materials_from_calc = QuantityMaterial.objects.filter(calculate=request.POST['calc_id'])
    calc = get_object_or_404(Calculate, id=request.POST['calc_id'])
    for key in request.POST:
        if 'price_' in key:
            mat_id = key.replace('price_', '')  # Отделяем ID материала
            material = materials_from_calc.get(id=int(mat_id))  # Достаем объект QuantityMaterial
            prise = float(request.POST[key])  # Получаем цену
            quantity = float(request.POST[f'quantity_{mat_id}'])  # Получаем колличество
            material.price = prise  # Присваиваем объекту QuantityMaterial цену
            material.quantity = quantity  # Присваиваем объекту QuantityMaterial коллличество
            material.amount = prise*quantity  # Определяем сумму
            # import ipdb; ipdb.set_trace()
            material.save()  # Сохраняем объект

    return HttpResponseRedirect(reverse('view_estimate_detail', kwargs={'slug': calc.slug}))


def total_price(materials, works):
    """Считаем ИТОГО по материалам и работам"""
    total_work_price = 0
    for work in works:
        total_work_price += work.amount

    total_material_price = 0
    for material in materials:
        total_material_price += material.amount

    return {'material': total_material_price, 'work': total_work_price}


class AddCalc(CreateView):
    """Создает новую смету"""
    queryset = Calculate.objects.all()
    models = Calculate
    fields = ['name', 'slug', 'text', 'difficulty_factor', 'fuel_price', 'tupe_calc', 'author']
    template_name = 'estimate/detail.html'

    def get_success_url(self):
        return reverse('view_estimate_detail')


class SearchMaterialListView(ListView):  # 
    """Поиск материалов для добавления в смету"""
    # context_object_name = 'materials'
    template_name = 'estimate/search.html'
    model = Material

    def get_queryset(self):  # Ищем материалы соответствующие запросу из формы
        query = self.request.GET.get('search_query')
        materials = Material.objects.filter(name__icontains=query)
        return materials
    
    def get_context_data(self, **kwargs):  # Добавляет в контекст шаблона слаг сметы в которую нужно добавить материал
        context = super().get_context_data(**kwargs)
        context['calc_id'] = self.request.GET['calc_id']  # Добавляем в контекст шаблона слаг сметы
        context['search_query'] = self.request.GET['search_query']  # Добавляем в контекст шаблона поисковый запрос
        return context


def add_material_to_calc(request, *args, **kwargs):
    """Добавляет материал в смету"""
    calc = get_object_or_404(Calculate, id=kwargs['calc_id'])
    material = get_object_or_404(Material, id=kwargs['pk'])
    QuantityMaterial.objects.create(  # Добавляем материал в список материалов
        material=material,
        calculate=calc,
        price=material.price,
        quantity=0
    )
    return HttpResponseRedirect(reverse('view_estimate_detail', kwargs={'slug': calc.slug}))
        

def delete_material_from_calc(request, *args, **kwargs):
    """Удаляет материал из сметы"""
    calc = get_object_or_404(Calculate, id=kwargs['calc_id'])
    QuantityMaterial.objects.filter(id=kwargs['pk']).delete()
    return HttpResponseRedirect(reverse('view_estimate_detail', kwargs={'slug': calc.slug}))
