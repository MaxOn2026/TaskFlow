from datetime import datetime, timezone
from typing import Any

import django
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.shortcuts import render

from tasks.models import Task


# Create your views here.
@login_required
def dashboard(request):
    all_tasks = Task.objects.all()
    new_tasks_today = all_tasks.filter(created_at=datetime.now().date()).count()

    total_tasks = all_tasks.count()

    # TODO доработать задачи "в работе", не отображаются в UI
    in_progress_tasks = all_tasks.filter(status__title='В работе').count()

    # TODO доработать completed_today, не отображаются в UI
    completed_tasks = all_tasks.filter(status__title='Завершена').count()
    completed_today = all_tasks.filter(status__is_final=True, completed_at__date=datetime.now().date()).count()

    overdue_tasks = return_overdue_cnt(all_tasks)

    # TODO исправить колонки(recent-недавние, отображаются внизу страницы, pending - в работе,
    #  отображаются в начале и в колонках. Возможно заменить pending на переиспользование in_progress_tasks)
    pending_tasks = all_tasks.order_by('-last_updated')[:5]
    recent_tasks = all_tasks.filter(status__title='В работе')

    context = {
        'new_tasks_today': new_tasks_today,
        'total_tasks': total_tasks,
        'in_progress_tasks': in_progress_tasks,
        'pending_tasks': recent_tasks,
        'completed_tasks': completed_tasks,
        'completed_today': completed_today,
        'overdue_tasks': overdue_tasks,
        'recent_tasks': recent_tasks
    }

    return render(request, 'dashboard/dashboard.html', context)


def return_overdue_cnt(all_tasks: QuerySet) -> int:
    overdue_tasks = []
    for task in all_tasks:
        if not task.status or task.status.title == 'completed':
            continue
        elif task.deadline < datetime.now(tz=timezone.utc):
            overdue_tasks.append(task)
    return len(overdue_tasks)