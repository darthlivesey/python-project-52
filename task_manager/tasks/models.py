from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    
    def __str__(self):
        return self.username


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True,
                             verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Дата создания")

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True,
                             verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Дата создания")
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_labels',
        verbose_name="Автор"
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                                verbose_name="Статус")
    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='created_tasks',
                                   verbose_name="Автор")
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name="Исполнитель"
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                       verbose_name="Дата создания")
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
        verbose_name="Метки"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']