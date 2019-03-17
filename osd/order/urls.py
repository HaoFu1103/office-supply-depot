from django.urls import path
from . import views

app_name = 'order'

url_patterns = [
    path('thanks/<int:order_id>/', views.thanks, name='thanks'),
]

