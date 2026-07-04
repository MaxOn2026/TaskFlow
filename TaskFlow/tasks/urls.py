from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('task_list/', views.get_task_list, name='task_list'),
    path('create_task/', views.create_task, name='create_task')
]
