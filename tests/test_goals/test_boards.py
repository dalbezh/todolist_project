import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import Board


@pytest.mark.django_db()
class TestRetrieveBoardView:

    @pytest.fixture(autouse=True)
    def setup(self, board, board_participant, user) -> None:
        board_participant.user = user
        board_participant.save()
        self.url = self.get_url(board)

    @staticmethod
    def get_url(board: Board) -> bytes:
        return reverse('goals:board', kwargs={'pk': board.pk})

    def test_auth_required(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
class TestCreateBoardView:
    url = reverse('goals:create_board')

    def test_auth_required(self, client):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_to_create_board(self, auth_client, faker):
        data = {"title": faker.sentence()}
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
