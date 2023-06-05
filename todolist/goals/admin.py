from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")
    readonly_fields = ("created", "updated")


class CommentsInline(admin.StackedInline):
    model = GoalComment
    extra = 0
    verbose_name = "Комментарий"
    verbose_name_plural = "Комментарии"


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "user", "status", "created", "updated")
    search_fields = ("title", "user")
    readonly_fields = ("created", "updated")
    inlines = [CommentsInline]
