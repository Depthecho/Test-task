from django.urls import path
from . import views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),

    path('create/', views.ad_create, name='ad_create'),
    path('edit/<int:ad_id>/', views.ad_edit, name='ad_edit'),
    path('delete/<int:ad_id>/', views.ad_delete, name='ad_delete'),

    path('exchange/proposals/', views.exchange_proposals_list, name='exchange_proposals_list'),
    path('exchange/create/<int:ad_id>/', views.create_exchange_proposal, name='create_exchange_proposal'),
    path('exchange/accept/<int:proposal_id>/', views.accept_exchange_proposal, name='accept_exchange_proposal'),
    path('exchange/reject/<int:proposal_id>/', views.reject_exchange_proposal, name='reject_exchange_proposal'),
]