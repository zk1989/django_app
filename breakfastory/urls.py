"""Defines URL patterns for breakfastory"""

from django.urls import path

from . import views

app_name = 'breakfastory'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    # Page that shows all meal types.
    path('mealtypes/', views.meal_types, name='meal_types'),
    # Detail page for a single meal type.
    path('mealtypes/<int:mealtype_id>/', views.meal_type, name='meal_type'),
    # Page for adding a new meal type.
    path('new_mealtype', views.new_meal_type, name='new_meal_type'),
]