from django.db import models
from django.utils import timezone

from core.models import User


class DatesModelMixin(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")


class GoalCategory(DatesModelMixin):

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title


class Goal(DatesModelMixin):

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(blank=True, verbose_name="Описание")
    category = models.ForeignKey(GoalCategory, on_delete=models.PROTECT, verbose_name="Категория")
    due_date = models.DateField(null=True, blank=True, verbose_name="Дедлайн")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.to_do, verbose_name="Статус"
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices, default=Priority.medium, verbose_name="Приоритет"
    )

    def __str__(self):
        return self.title


class GoalComment(DatesModelMixin):

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, verbose_name="Цель")
    text = models.TextField(verbose_name="Текст комментария")
