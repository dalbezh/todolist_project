from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import Goal
from goals.serializers import GoalCreateSerializer, GoalSerializer
from goals.filters import GoalDateFilter
from goals.permissions import GoalPermission


class GoalCreateView(CreateAPIView):
    """
    Создание цели
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    """
    Список целей
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=Goal.Status.archived)


class GoalView(RetrieveUpdateDestroyAPIView):
    """
    Редактирование или удаление целей
    """
    serializer_class = GoalSerializer
    permission_classes = [GoalPermission]
    queryset = Goal.objects.exclude(status=Goal.Status.archived)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
