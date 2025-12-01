from django.urls import path
from . import views

urlpatterns = [
    path('', views.grn_list, name='grn_list'),
    path('<int:pk>/', views.grn_detail, name='grn_detail'),
]
