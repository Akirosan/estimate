from django.shortcuts import render
from .models import Calculate, Material, QuantityMaterial, QuantityWork

def view_list(request):
    """Вывод списка смет"""
    estimate = Calculate.objects.all()
    return render(request, 'estimate/list.html', {'calculate': estimate})


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
