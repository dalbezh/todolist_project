from django.db import migrations, transaction
from django.utils import timezone


def create_objects(apps, schema_editor):

    User = apps.get_model("core", "User")
    Board = apps.get_model("goals", "Board")
    BoardParticipant = apps.get_model("goals", "BoardParticipant")
    GoalCategory = apps.get_model("goals", "GoalCategory")

    with transaction.atomic():
        for user_id in User.objects.values_list("id", flat=True):
            new_board = Board.objects.create(
                title="Мои цели",
                created=timezone.now(),
                updated=timezone.now()
            )
            BoardParticipant.objects.create(
                user_id=user_id,
                board=new_board,
                role=1,
                created=timezone.now(),
                updated=timezone.now()
            )

            GoalCategory.objects.filter(user_id=user_id).update(board=new_board)


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_board_goalcategory_board_boardparticipant'),
    ]

    operations = [
        migrations.RunPython(create_objects, migrations.RunPython.noop)
    ]
