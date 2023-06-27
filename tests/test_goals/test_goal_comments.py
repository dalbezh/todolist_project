import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import GoalComment



@pytest.mark.django_db()
class TestRetrieveGoalComment:

    @pytest.fixture(autouse=True)
    def setup(self, goal_comment, board_participant, user) -> None:
        board_participant.user = user
        board_participant.save()
        self.url = self.get_url(goal_comment)

    @staticmethod
    def get_url(comment: GoalComment) -> bytes:
        return reverse('goals:comment', kwargs={'pk': comment.pk})

    def test_auth_required(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
