from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager.tasks'
    verbose_name = _("Task Manager")
