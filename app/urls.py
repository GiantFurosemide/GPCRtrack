from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    #path('login/', views.login_view, name='login'),
    path('entry/', views.entry, name='entry'),
    path('entry_success/', views.entry_success, name='entry_success'),
    path('search/', views.search, name='search'),
    path('apply/<str:construct_number>/', views.apply, name='apply'),
    path('apply_success/', views.apply_success, name='apply_success'),
    path('edit/<str:construct_number>/', views.edit, name='edit'),
    path('delete/<str:construct_number>/', views.delete, name='delete'),
    path('application/', views.application, name='application'),
    path('export/', views.export, name='export'),
    path('statistics/', views.statistics, name='statistics'),
]
