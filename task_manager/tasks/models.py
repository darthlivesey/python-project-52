from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation date")
    )
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Status(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation date")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")


class Label(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation date")
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_labels',
        verbose_name=_("Creator")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")


class Task(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_("Status")
    )
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_tasks',
        verbose_name=_("Creator")
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=_("Executor")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Creation date")
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
        verbose_name=_("Labels")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ['-created_at']