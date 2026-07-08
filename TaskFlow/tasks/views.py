from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .forms import TaskForm
from .models import Task

# Create your views here.
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def get_task_list(request):
    all_tasks = Task.objects.all()

    paginator = Paginator(all_tasks, 10)

    page_number = request.GET.get('page', 1)

    current_page = paginator.get_page(page_number)
    context = {
        'tasks': all_tasks,
        'current_page': current_page
    }

    return render(request, 'tasks/task_list.html', context)

@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(data=request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('tasks:task_list')
