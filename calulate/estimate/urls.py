from django.contrib import admin
from django.urls import path, include
from .views import (view_detail, CalcListView,
                    login, CatalogMaterialsView,
                    CatalogWorksView, AddMaterial,
                    EditMaterial, DeleteMaterial, AddCalc,
                    SearchMaterialListView)

urlpatterns = [
    
    path('add/', AddCalc.as_view(), name='add_calc'), # Создать смету
    path('<slug:slug>/', view_detail, name='view_estimate_detail'),
    path('estimate_list/', CalcListView.as_view(), name='view_estimate_list'),
    path('', CalcListView.as_view(), name='view_estimate_list'),
    path('login', login, name='login'),
    path('material', CatalogMaterialsView.as_view(), name='catalog_materials'),
    path('works', CatalogWorksView.as_view(), name='catalog_works'),

    path('material/add/', AddMaterial.as_view(), name='add_material'),
    path('material/<int:pk>/edit/', EditMaterial.as_view(), name='edit_material'),
    path('material/<int:pk>/delete/', DeleteMaterial.as_view(), name='delete_material'),

    path('material/search/', SearchMaterialListView.as_view(), name='search_material'),

    

    # path('', view_list, name='view_estimate_list'),
    # path('estimate/', include('estimate.urls')),
]