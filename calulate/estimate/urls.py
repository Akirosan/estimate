from django.contrib import admin
from django.urls import include, path

from .views import (AddCalc, AddMaterial, CalcListView, CatalogMaterialsView,
                    CatalogWorksView, DeleteMaterial, EditMaterial,
                    SearchMaterialListView, add_material_to_calc,
                    delete_material_from_calc, edit_mat_in_calc, login,
                    view_detail)

urlpatterns = [
    
    path('add/', AddCalc.as_view(), name='add_calc'),  # Создать смету
    path('<slug:slug>/', view_detail, name='view_estimate_detail'),
    path('estimate_list/', CalcListView.as_view(), name='view_estimate_list'),
    path('', CalcListView.as_view(), name='view_estimate_list'),
    path('login', login, name='login'),
    # Каталог материалов
    path('material', CatalogMaterialsView.as_view(), name='catalog_materials'),
    # Каталог видов работ
    path('works', CatalogWorksView.as_view(), name='catalog_works'),
    # Добавление материала в каталог материалов
    path('material/add/', AddMaterial.as_view(), name='add_material'),
    # Редакт мат. в каталоге материалов
    path(
        'material/<int:pk>/edit/',
        EditMaterial.as_view(),
        name='edit_material'
    ),
    path(  # Удаление материала из каталож
        'material/<int:pk>/delete/',
        DeleteMaterial.as_view(),
        name='delete_material'
    ),
    path(  # Поиск материала
        'material/search/',
        SearchMaterialListView.as_view(),
        name='search_material'),
    path(  # Добавление материала в смету
        '<int:pk>/add_to_calc/<int:calc_id>/',
        add_material_to_calc,
        name='add_material_to_calc'
    ),
    path(  # Удаление материала из сметы
        '<int:pk>/delete_from_calc/<int:calc_id>/',
        delete_material_from_calc,
        name='delete_material_from_calc'
    ),
    path(  # Изменяет цену и количество материала в смете
        'matedit/edit-mat-in-calc/',
        edit_mat_in_calc,
        name='edit_mat_in_calc'
    ),

]
