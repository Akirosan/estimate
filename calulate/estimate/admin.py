from django.contrib import admin
from django.db import models
from django.db.models import fields
from .models import (Tag, Work, Calculate, 
                    Favorite, Material, QuantityMaterial, 
                    QuantityWork
                    )
class WorkInline(admin.TabularInline):
    model = Calculate.work.through
    extra = 1



class MaterialInline(admin.TabularInline):
    model = Calculate.material.through
    extra = 1




@admin.register(Calculate)
class CalculateAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_create', 'date_update', 'author',  'tupe_calc')
    inlines = [WorkInline, MaterialInline]
    prepopulated_fields = {'slug':('name',)}
    fieldsets = (
        ('Основное', {'fields': ('name', 'author', 'slug', 'text' )}),
        ('Дополнительно', {'fields': ('difficulty_factor', 'fuel_price', 'upload', 'tag', 'tupe_calc')}),
    )


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'price')
    search_fields = ('name', )


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'price')
    search_fields = ('name', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'calculate',)
