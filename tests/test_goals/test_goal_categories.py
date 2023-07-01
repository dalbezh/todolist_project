import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import BoardParticipant
from .factories import CreateGoalCategoryRequest
from goals.models import GoalCategory


@pytest.mark.django_db()
class TestRetrieveGoalCategory:

    @pytest.fixture(autouse=True)
    def setup(self, goal_category, board_participant, user) -> None:
        board_participant.user = user
        board_participant.save()
        self.url = self.get_url(goal_category)

    @staticmethod
    def get_url(category: GoalCategory) -> bytes:
        return reverse('goals:category', kwargs={'pk': category.pk})

    def test_auth_required(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db()
class TestCreateCategoryView:
    url = reverse('goals:create_category')

    def test_auth_required(self, client):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_to_create_category(self, auth_client, board, faker):
        data = CreateGoalCategoryRequest.build(board=board.id)
        response = auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.usefixtures('board_participant')
    def test_create_category_on_deleted_category(self, auth_client, board):
        board.is_deleted = True
        board.save(update_fields=(['is_deleted']))
        data = CreateGoalCategoryRequest.build(board=1)
        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'board': ['Invalid pk "1" - object does not exist.']}

    @pytest.mark.usefixtures('board_participant')
    def test_create_category_on_not_existing_board(self, auth_client):
        data = CreateGoalCategoryRequest.build(category=1)

        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'board': ['This field is required.']}

    @pytest.mark.parametrize(
        'role',
        [BoardParticipant.Role.owner, BoardParticipant.Role.writer],
        ids=['owner', 'writer']
    )
    def test_have_to_create_to_with_roles_owner_or_writer(
            self, auth_client, board_participant, board, faker, role
    ):
        board_participant.role = role
        board_participant.save(update_fields=['role'])
        # data = {'board': board_participant.id, 'title': faker.sentence()}
        data = CreateGoalCategoryRequest.build(board=board.id)
        response = auth_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
