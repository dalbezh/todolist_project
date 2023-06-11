from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalComment
from goals.serializers import GoalCommentCreateSerializer, GoalCommentSerializer
from goals.permissions import GoalCommentPermission


class GoalCommentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_fields = ["goal"]
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    serializer_class = GoalCommentSerializer
    permission_classes = [GoalCommentPermission]
    queryset = GoalComment.objects.select_related("user")

    def get_queryset(self):
        return GoalComment.objects.select_related("user").filter(
            goal__category__board__participants__user=self.request.user
        )