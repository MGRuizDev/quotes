
from django.urls import path
from .views import *
app_name='quoting'
urlpatterns = [
    path('', home, name='home'),
    path('create/', create),
    path('<slug>/', detail, name = 'detail'),
    path('<slug>/update/', update, name= 'update'),
    path('<slug>/delete', delete),
]
