from django.db import transaction
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView

from goals.permissions import BoardPermission
from goals.serializers import BoardListSerializer, BoardSerializer
from goals.models import Board, BoardParticipant, Goal


class BoardCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardListSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(
                user=self.request.user,
                board=board,
                role=BoardParticipant.Role.owner
            )


class BoardListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardListSerializer
    filter_backends = [OrderingFilter]
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user).exclude(is_deleted=True)


class BoardView(RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardSerializer
    queryset = Board.objects.prefetch_related('participants__user').exclude(is_deleted=True)

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            Board.objects.filter(id=instance.id).update(is_deleted=True)
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
