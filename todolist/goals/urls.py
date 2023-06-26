from django.urls import path

from goals.views.goal_category import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.goal import GoalCreateView, GoalListView, GoalView
from goals.views.goal_comment import GoalCommentCreateView, GoalCommentListView, GoalCommentView
from goals.views.board import BoardCreateView, BoardListView, BoardView

app_name = 'goals'

urlpatterns = [
    path("goal_category/create", GoalCategoryCreateView.as_view(), name="create_category"),
    path("goal_category/list", GoalCategoryListView.as_view(), name="list_categories"),
    path("goal_category/<pk>", GoalCategoryView.as_view(), name="category"),
    path("goal/create", GoalCreateView.as_view(), name="create_goal"),
    path("goal/list", GoalListView.as_view(), name="list_goal"),
    path("goal/<pk>", GoalView.as_view(), name="goal"),
    path("goal_comment/create", GoalCommentCreateView.as_view(), name="create_comment"),
    path("goal_comment/list", GoalCommentListView.as_view(), name="list_comments"),
    path("goal_comment/<pk>", GoalCommentView.as_view(), name="comment"),
    path("board/create", BoardCreateView.as_view(), name="create_board"),
    path("board/list", BoardListView.as_view(), name="list_boards"),
    path("board/<pk>", BoardView.as_view(), name="board"),
]
