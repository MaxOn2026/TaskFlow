
from django.db import models
from django.conf import settings

# Create your models here.


class Status(models.Model):
    title = models.CharField(max_length=64)
    is_final = models.BooleanField(default=False)
    color = models.CharField(
        max_length=7 #  #RRGGBB(HEX)
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Task(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        related_name='status',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Владелец'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"