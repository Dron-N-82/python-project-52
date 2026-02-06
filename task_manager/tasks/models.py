from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.users.models import User

from ..labels.models import Label


# Create your models here.
class Task(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        unique=True,
        verbose_name=_('Name')
        )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
    )
    executor = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        verbose_name=_('Executor'),
        related_name='task_executor',
        )
    author = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name=_('Author'),
        related_name='task_author'
        )
    status = models.ForeignKey(
        Status,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name=_('Status'),
        related_name='tasks'
        )
    label = models.ManyToManyField(
        Label,
        blank=True,
        verbose_name=_('Label'),
        related_name='tasks'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date'),
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
