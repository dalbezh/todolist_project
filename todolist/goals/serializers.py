from django.db import transaction
from rest_framework import serializers

from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant
from core.serializers import ProfileSerializer
from core.models import User


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Category not found")

        if not BoardParticipant.objects.filter(
                board_id=value.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context["request"].user
        ).exists():
            raise serializers.ValidationError("Permission Denied")

        return value

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, board):
        if board.is_deleted:
            raise serializers.ValidationError("Board is deleted")

        if not BoardParticipant.objects.filter(
            board_id=board.id,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
            user_id=self.context["request"].user
        ).exists():
            raise serializers.ValidationError("Permission Denied")
        return board

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_goal(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Goal not found")

        if not BoardParticipant.objects.filter(
                board_id=value.category.board_id,
                role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                user_id=self.context["request"].user
        ).exists():
            raise serializers.ValidationError("Permission Denied")
        return value

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalSerializer(GoalCreateSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

class GoalCategorySerializer(GoalCategoryCreateSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentSerializer(GoalCommentCreateSerializer):
    user = ProfileSerializer(read_only=True)
    goal = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "is_deleted")


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.editable_choices
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    def validate_user(self, user):
        if self.context['request'].user == user:
            raise serializers.ValidationError("Failed to change your role")

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
#    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

#    def update(self, instance, validated_data):
#        owner = validated_data.pop("user")
#        new_participants = validated_data.pop("participants")
#        new_by_id = {part["user"].id: part for part in new_participants}
#
#        old_participants = instance.participants.exclude(user=owner)
#        with transaction.atomic():
#            for old_participant in old_participants:
#                if old_participant.user_id not in new_by_id:
#                    old_participant.delete()
#                else:
#                    if old_participant.role != new_by_id[old_participant.user_id]["role"]:
#                        old_participant.role = new_by_id[old_participant.user_id]["role"]
#                        old_participant.save()
#                    new_by_id.pop(old_participant.user_id)
#            for new_part in new_by_id.values():
#                BoardParticipant.objects.create(board=instance, user=new_part["user"], role=new_part["role"])
#
#            instance.title = validated_data["title"]
#            instance.save()
#
#        return instance

    def update(self, instance: Board, validated_data: dict) -> Board:
        request = self.context['request']
        with transaction.atomic():
            BoardParticipant.objects.filter(board=instance).exclude(user=request.user).delete()
            BoardParticipant.objects.bulk_create(
                [
                    BoardParticipant(user=participant['user'], role=participant['role'], board=instance)
                    for participant in validated_data.get('participants', [])
                ],
                ignore_conflicts=False,
            )
            if title := validated_data.get('title'):
                instance.title = title
            instance.save()
        return instance