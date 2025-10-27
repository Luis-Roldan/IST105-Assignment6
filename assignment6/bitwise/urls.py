from django.urls import path
from . import views

app_name = 'bitwise'

urlpatterns = [
    path('', views.index, name='index'),
    path('entries/', views.view_all_entries, name='view_entries'),
]
