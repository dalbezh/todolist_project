from rest_framework.generics import GenericAPIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from goals.models import Goal, GoalCategory, GoalComment, BoardParticipant, Board


class BoardPermission(IsAuthenticated):
    def has_object_permission(self, request, view: GenericAPIView, obj: Board) -> bool:
        _filters = {"user": request.user, "board": obj}
        if request.method not in SAFE_METHODS:
            _filters["role"] = BoardParticipant.Role.owner
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermission(IsAuthenticated):
    def has_object_permission(self, request, view: GenericAPIView, obj: GoalCategory) -> bool:
        _filters = {"user": request.user, "board": obj.board}
        if request.method not in SAFE_METHODS:
            _filters["role__in"] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalPermission(IsAuthenticated):
    def has_object_permission(self, request, view: GenericAPIView, obj: Goal) -> bool:
        _filters = {"user": request.user, "board": obj.category.board}
        if request.method not in SAFE_METHODS:
            _filters["role__in"] = [BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCommentPermission(IsAuthenticated):
    def has_object_permission(self, request, view: GenericAPIView, obj: GoalComment) -> bool:
        if request.method is SAFE_METHODS:
            return True
        return obj.user == request.user
