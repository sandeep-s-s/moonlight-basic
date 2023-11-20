from django.urls import path
from .views import index,index_action

urlpatterns = [
    path('', index, name='index'),
    path('index-action/', index_action, name='index-action'),
]
