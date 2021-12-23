from django.contrib import admin
from django.urls import path, include
from .views import view_list, view_detail

urlpatterns = [
    
    path('<slug:slug>/', view_detail, name='view_estimate_detail'),
    path('', view_list, name='view_estimate_list'),
    # path('estimate/', include('estimate.urls')),
]