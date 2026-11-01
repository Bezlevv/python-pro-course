from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('modules/', views.module_list, name='modules'),
    path('modules/<slug:module_slug>/', views.module_detail, name='module_detail'),
    path('modules/<slug:module_slug>/<slug:lesson_slug>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]
