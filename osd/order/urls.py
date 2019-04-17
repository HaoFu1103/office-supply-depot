from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('thanks/', views.thanks, name='thanks'),
]


"""<int:order_id>/"""
