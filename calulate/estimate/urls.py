from django.contrib import admin
from django.urls import path, include
from .views import (view_detail, CalcListView,
                    login, CatalogMaterialsView,
                    CatalogWorksView, AddMaterial,
                    EditMaterial, DeleteMaterial, AddCalc,
                    SearchMaterialListView,
                    add_material_to_calc, delete_material_from_calc,
                    edit_mat_in_calc)

urlpatterns = [
    
    path('add/', AddCalc.as_view(), name='add_calc'),  # Создать смету
    path('<slug:slug>/', view_detail, name='view_estimate_detail'),
    path('estimate_list/', CalcListView.as_view(), name='view_estimate_list'),
    path('', CalcListView.as_view(), name='view_estimate_list'),
    path('login', login, name='login'),
    path('material', CatalogMaterialsView.as_view(), name='catalog_materials'),  # Каталог материалов
    path('works', CatalogWorksView.as_view(), name='catalog_works'),  # Каталог видов работ
    
    path('material/add/', AddMaterial.as_view(), name='add_material'),  # Добавление материала в каталог материалов
    path('material/<int:pk>/edit/', EditMaterial.as_view(), name='edit_material'),  # Редакт мат. в каталоге материалов
    path('material/<int:pk>/delete/', DeleteMaterial.as_view(), name='delete_material'),  # Удаление материала из катал

    path('material/search/', SearchMaterialListView.as_view(), name='search_material'),  # Поиск материала

    path('<int:pk>/add_to_calc/<int:calc_id>/', add_material_to_calc, name='add_material_to_calc'),  # Добавление
    path('<int:pk>/delete_from_calc/<int:calc_id>/', delete_material_from_calc, name='delete_material_from_calc'),

    path('matedit/edit-mat-in-calc/', edit_mat_in_calc, name='edit_mat_in_calc'),  # Изменяет цену и количество

]
