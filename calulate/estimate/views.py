from multiprocessing import context
from tkinter import N
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView
from .forms import AddWorkForm, SearchMaterialForm

from .models import Calculate, Material, QuantityMaterial, QuantityWork, Work


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


def add_work(request):
    if request.method == 'POST':
        form = AddWorkForm(request.POST)  # Передаем данные из POST в форму
        if form.is_valid():  # Если проверка успешна
            new_work = Work(
                name = form.cleaned_data['name'],
                measurement_unit = form.cleaned_data['measurement_unit'],
                price = form.cleaned_data['price']
            )
            new_work.save()
            # import ipdb; ipdb.set_trace()
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        form = AddWorkForm()
    return HttpResponseRedirect(request.META['HTTP_REFERER'], {'form': form})

# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')
#     else:
#         form = NameForm()

#     return render(request, 'name.html', {'form': form})








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
    # import ipdb; ipdb.set_trace()
    scroll = ""
    if 'scroll' in request.GET:
        scroll = request.GET['scroll']
    
    return render(
        request, 'estimate/detail.html', {
            'calculate': calculate,
            'materials': materials,
            'works': works,
            'total': total_price(materials, works),
            'scroll': scroll
        }
    )


def edit_mat_in_calc(request, *args, **kwargs):
    """Редактирует материалы и работы в смете сметы"""
    calc = get_object_or_404(Calculate, id=request.POST['calc_id'])
    materials_from_calc = QuantityMaterial.objects.filter(
        calculate=request.POST['calc_id']
    )
    for key in request.POST:
        if 'mat_price_' in key:
            mat_id = key.replace('mat_price_', '')  # Отделяем ID материала
            material = materials_from_calc.get(id=int(mat_id))
            prise = float(request.POST[key])  # Получаем цену
            quantity = float(request.POST[f'mat_quantity_{mat_id}'])  # колличество
            material.price = prise  # Присваиваем объекту QuantityMaterial цену
            material.quantity = quantity  # Присваиваем объекту коллличество
            material.amount = prise * quantity  # Определяем сумму
            material.save()  # Сохраняем объект
    return HttpResponseRedirect(
        reverse('view_estimate_detail', kwargs={'slug': calc.slug})
    )

def edit_work_in_calc(request, *args, **kwargs):
    calc = get_object_or_404(Calculate, id=request.POST['calc_id'])
    works_from_calc = QuantityWork.objects.filter(
        calculate=request.POST['calc_id']
    )
    for key in request.POST:
        if 'work_price_' in key:
            work_id = key.replace('work_price_', '')  # Отделяем ID вида работы
            work = works_from_calc.get(id=int(work_id))
            price = float(request.POST[key])  # Получаем цену
            quantity = float(request.POST[f'work_quantity_{work_id}'])  # колличество
            work.price = price  # Присваиваем объекту QuantityMaterial цену
            work.quantity = quantity  # Присваиваем объекту коллличество
            work.amount = price * quantity  # Определяем сумму
            work.save()  # Сохраняем объект
    return HttpResponseRedirect(
        reverse('view_estimate_detail', kwargs={'slug': calc.slug})
    )


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
    fields = [
        'name',
        'slug',
        'text',
        'difficulty_factor',
        'fuel_price',
        'tupe_calc',
        'author'
    ]
    template_name = 'estimate/detail.html'

    def get_success_url(self):
        return reverse('view_estimate_detail')


class SearchMaterialListView(ListView):
    """Поиск материалов для добавления в смету"""
    # context_object_name = 'materials'
    template_name = 'estimate/search.html'
    model = Material

    def get_queryset(self):  # Ищем материалы соответствующие запросу из формы
        # import ipdb; ipdb.set_trace()
        query = self.request.GET.get('search_query')
        search_data = Material.objects.filter(name__icontains=query)
        return search_data

    def get_context_data(self, **kwargs):
        """Добавляет в контекст слаг сметы в которую нужно добавить материал"""
        # import ipdb; ipdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['calc_id'] = self.request.GET['calc_id']
        context['search_query'] = self.request.GET['search_query']
        context['search_type'] = "mat"
        return context


def add_object_to_calc(request, *args, **kwargs):
    """Добавляет материал/работу в смету"""
    calc = get_object_or_404(Calculate, id=kwargs['calc_id'])
    if kwargs['search_type'] == "mat":
        material = get_object_or_404(Material, id=kwargs['pk'])
        QuantityMaterial.objects.create(
            material=material,
            calculate=calc,
            price=material.price,
            quantity=0
        )
    if kwargs['search_type'] == "work":
        work = get_object_or_404(Work, id=kwargs['pk'])
        QuantityWork.objects.create(
            work=work,
            calculate=calc,
            price=work.price,
            quantity=0
        )
    if 'scroll' in kwargs:
        scroll = f'?scroll={kwargs["scroll"]}'  # Заберем значение scroll из именованных и отправим GET запросом в обработчик view_estimate_detail
        return HttpResponseRedirect(reverse('view_estimate_detail', kwargs={'slug': calc.slug}) + scroll)
    return HttpResponseRedirect(reverse('view_estimate_detail', kwargs={'slug': calc.slug}))



def delete_material_from_calc(request, *args, **kwargs):
    """Удаляет материал из сметы"""
    calc = get_object_or_404(Calculate, id=kwargs['calc_id'])
    QuantityMaterial.objects.filter(id=kwargs['pk']).delete()
    return HttpResponseRedirect(
        reverse('view_estimate_detail', kwargs={'slug': calc.slug})
    )



class SearchWorkListView(ListView):
    """Поиск работ для добавления в смету"""
    template_name = 'estimate/search.html'
    model = Work

    def get_queryset(self):  # Ищем материалы соответствующие запросу из формы
        query = self.request.GET.get('search_query')
        search_data = Work.objects.filter(name__icontains=query)
        return search_data

    def get_context_data(self, **kwargs):
        """Добавляет в контекст слаг сметы в которую нужно добавить работу"""
        context = super().get_context_data(**kwargs)
        context['calc_id'] = self.request.GET['calc_id']
        context['scroll'] = self.request.GET['scroll']
        context['search_query'] = self.request.GET['search_query']  # Поисковый запрос
        context['search_type'] = "work"  # Идентификатор объекта поиска (работа или материал)
        return context

def delete_work_from_calc(request, *args, **kwargs):
    """Удаляет материал из сметы"""
    calc = get_object_or_404(Calculate, id=kwargs['calc_id'])
    QuantityWork.objects.filter(id=kwargs['pk']).delete()
    return HttpResponseRedirect(
        reverse('view_estimate_detail', kwargs={'slug': calc.slug})
    )