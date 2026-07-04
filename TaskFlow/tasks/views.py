from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import TaskForm
from .models import Task

# Create your views here.

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

def get_task_list(request):
    all_tasks = Task.objects.all()

    paginator = Paginator(all_tasks, 10)

    page_number = request.GET.get('page', 1)

    current_page = paginator.get_page(page_number)
    context = {
        'current_page': current_page
    }

    return render(request, 'tasks/task_list.html', context)
