from django.urls import path
from . import views

urlpatterns = [
    path('', views.pr_list, name='pr_list'),
    path('<int:pk>/', views.pr_detail, name='pr_detail'),
]
