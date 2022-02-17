from django.urls import path

from .views import (AddCalc, AddMaterial, CalcListView, CatalogMaterialsView,
                    CatalogWorksView, DeleteMaterial, EditMaterial,
                    SearchMaterialListView, add_object_to_calc,
                    delete_material_from_calc, edit_mat_in_calc, login,
                    view_detail, edit_work_in_calc, SearchWorkListView, add_work, 
                    delete_work_from_calc,)

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
    
    path(  # Редакт мат. в каталоге материалов
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
        '<int:calc_id>/add_to_calc/<str:search_type>/<int:pk>/<int:scroll>/',
        add_object_to_calc,
        name='add_object_to_calc'
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


    path(  # Изменяет цену и количество материала в смете
        'matedit/edit_work_in_calc/',
        edit_work_in_calc,
        name='edit_work_in_calc'
    ),
    path(  # Поиск вида работ
        'work/search/',
        SearchWorkListView.as_view(),
        name='search_work'),
    # Добавление материала в каталог материалов
    path('work/add/', add_work, name='add_work'),
    path(  # Удаление материала из сметы
        '<int:calc_id>/work/delete/<int:pk>/',
        delete_work_from_calc,
        name='delete_work_from_calc'
    ),
    # path(  # Удаление материала из сметы
    #     '<slug:slug>/',
    #     list_calc_after_add_object,
    #     name='list_calc_after_add_object'
    # ),
    

]
