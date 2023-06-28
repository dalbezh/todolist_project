import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import GoalComment

from goals.models import BoardParticipant


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


@pytest.mark.django_db()
class TestCreateCommentView:
    url = reverse('goals:create_comment')

    def test_auth_required(self, client):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_to_create_comment(self, auth_client, goal, faker, user):
        data = {'goal': goal.id, 'text': faker.sentence()}
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Permission Denied'}

    def test_failed_to_create_board_if_reader(self, auth_client, board_participant, goal, faker):
        board_participant.role = BoardParticipant.Role.reader
        board_participant.save(update_fields=['role'])
        data = {'goal': goal.id, 'text': faker.sentence()}
        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Permission Denied'}

    @pytest.mark.usefixtures('board_participant')
    def test_create_category_on_not_existing_board(self, auth_client, goal, faker):
        data = {'goal': 1, 'text': faker.sentence()}

        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'goal': ['Invalid pk "1" - object does not exist.']}

