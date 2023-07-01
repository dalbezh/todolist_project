from django.db import transaction
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalCategory, Goal
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer
from goals.permissions import GoalCategoryPermission


class GoalCategoryCreateView(CreateAPIView):
    """
    Создание категории
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """
    Список категорий
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCategorySerializer
    filter_backends = [
        OrderingFilter,
        SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(board__participants__user=self.request.user).exclude(is_deleted=True)


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    Просмотр, редактирование или удаление категории
    """
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermission]
    queryset = GoalCategory.objects.exclude(is_deleted=True)

    def perform_destroy(self, instance):
        """Атомарное исполнение"""
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=["is_deleted"])
            instance.goal_set.update(status=Goal.Status.archived)
