from django.urls import path
from . import views

urlpatterns = [
    path('', views.rp_list, name='rp_list'),
    path('<int:pk>/', views.rp_detail, name='rp_detail'),
]
