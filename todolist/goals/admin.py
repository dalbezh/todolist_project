from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class BaseAdmin(admin.ModelAdmin):
    search_fields = ("title", )
    readonly_fields = ("created", "updated")


@admin.register(GoalCategory)
class GoalCategoryAdmin(BaseAdmin):
    list_display = ("title", "user", "created", "updated")


class CommentsInline(admin.StackedInline):
    model = GoalComment
    extra = 1
    verbose_name = "Комментарий"
    verbose_name_plural = "Комментарии"


@admin.register(Goal)
class GoalAdmin(BaseAdmin):
    list_display = ("title", "category", "user", "status", "created", "updated")
    inlines = [CommentsInline]


@admin.register(Board)
class BoardAdmin(BaseAdmin):
    list_display = ("title", "created", "updated")
    list_display_links = ["title"]
    search_fields = ("title", )


@admin.register(BoardParticipant)
class BoardParticipantAdmin(BaseAdmin):
    list_display = ("board", "user", "role", "created", "updated")
    search_fields = ("title", )
