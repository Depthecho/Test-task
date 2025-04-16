from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.ad_create, name='ad_create'),
    path('edit/<int:ad_id>/', views.ad_edit, name='ad_edit'),
    path('delete/<int:ad_id>/', views.ad_delete, name='ad_delete'),
]