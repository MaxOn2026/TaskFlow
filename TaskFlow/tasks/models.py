from datetime import datetime, timedelta, timezone

from django.db import models
from django.conf import settings

# Create your models here.
from django.contrib.auth.models import User

class Status(models.Model):
    title = models.CharField(max_length=64)
    is_final = models.BooleanField(default=False)
    color = models.CharField(
        max_length=7 #  #RRGGBB(HEX)
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(
        Status,
        null=True,
        default=1,
        on_delete=models.SET_NULL,
        related_name='status',
        verbose_name='Статус'
    )

    # TODO необходимо реализовать изменение дедлайна
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(default=datetime.now(tz=timezone.utc) + timedelta(days=1))
    completed_at = models.DateTimeField(null=True, blank=True)

    # TODO необходимо реализовать сортировку задач по пользователю; возможность назначать задачи на других людей
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='user',
        verbose_name='Владелец'
    )

    # TODO проверить, где используется и удалить при необходимости
    @property
    def is_completed(self):
        if not self.status or not self.completed_at:
            return False
        return (
            self.status.is_final
            and self.completed_at.date() == datetime.now().date()
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

class OwnersTasks(models.Model):
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)