from django.urls import path
from . import views

urlpatterns = [
    path('', views.po_list, name='po_list'),
    path('<int:pk>/', views.po_detail, name='po_detail'),
]
