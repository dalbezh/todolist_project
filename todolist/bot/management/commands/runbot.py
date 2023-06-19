import logging

from django.core.management import BaseCommand
from django.utils.crypto import get_random_string

from bot.tg.client import TgClient
from bot.tg.dc import Message, FSMData
from bot.tg.render import render_template
from bot.models import TgUser

from goals.models import Goal, GoalCategory



COMMANDS = ["/start", "/create", "/goals"]

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.client: [int, FSMData] = {}

    def handle(self, *args, **options):
        offset = 0
        self.stdout.write(self.style.SUCCESS("Bot started"))
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)
                # logging
                logger.debug(item.message)

    def handle_message(self, message: Message):
        tg_user, _ = TgUser.objects.get_or_create(chat_id=message.chat.id)
        if tg_user.user:
            self.handle_authorized_user(tg_user, message)
        else:
            self.handle_unauthorized_user(tg_user, message)

    def handle_unauthorized_user(self, tg_user: TgUser, message: Message):
        chat_id = tg_user.chat_id

        if message.text == "/start":

            verification_code = get_random_string(20)
            tg_user.verification_code = verification_code
            tg_user.save(update_fields=["verification_code"])

            text = render_template(
                "start.j2",
                user=message.chat.username,
                verification_code=tg_user.verification_code
            )
            self.tg_client.send_message(chat_id=chat_id, text=text)
        else:
            self.handle_available_list_commands(tg_user, message, "command_not_found.j2")

    def handle_authorized_user(self, tg_user: TgUser, message: Message):
        if message.text.startswith("/"):
            if message.text == "/goals":
                self.handle_goals_command(tg_user, message)
            elif message.text == "/create":
                self.handle_create_command(tg_user, message)
            elif message.text == "/cancel" and tg_user.chat_id in self.client:
                self.client.pop(tg_user.chat_id, None)
                self.tg_client.send_message(chat_id=tg_user.chat_id, text="Отменено")
            elif message.text == "/start":
                self.tg_client.send_message(chat_id=tg_user.chat_id, text="Вы уже верифицированы")
                self.handle_available_list_commands(tg_user, message, "command_list.j2")
            else:
                self.handle_available_list_commands(tg_user, message, "command_list.j2")
        elif tg_user.chat_id in self.client:
            client = self.client[tg_user.chat_id]
            client.next_handler(tg_user, message, **client.data)

    def handle_goals_command(self, tg_user: TgUser,  message: Message):
        goals = Goal.objects.filter(user=tg_user.user).exclude(status=Goal.Status.archived)
        if goals:
            text = render_template("goals_list.j2", goals=goals)
        else:
            text = "У вас нет целей"
        self.tg_client.send_message(chat_id=tg_user.chat_id, text=text)

    def handle_create_command(self, tg_user: TgUser,  message: Message):
        categories = GoalCategory.objects.filter(user=tg_user.user).exclude(is_deleted=True)
        if not categories:
            self.tg_client.send_message(chat_id=tg_user.chat_id, text="У вас нет доступных категорий")
            return
        else:
            text = render_template("catigories_list.j2", categories=categories)
            self.tg_client.send_message(chat_id=tg_user.chat_id, text=text)
            self.client[tg_user.chat_id] = FSMData(next_handler=self._get_category, data={'category': categories})

    def _get_category(self, tg_user: TgUser, message: Message, **kwargs):
        try:
            category = GoalCategory.objects.get(pk=message.text)
        except GoalCategory.DoesNotExist:
            self.tg_client.send_message(tg_user.chat_id, 'Данной категории нет')
        else:
            self.client[tg_user.chat_id] = FSMData(next_handler=self._create_goal, data={'category': category})
            self.tg_client.send_message(tg_user.chat_id, 'Введите название цели')

    def _create_goal(self, tg_user: TgUser, message: Message, **kwargs):
        category = kwargs['category']
        Goal.objects.create(category=category, user=tg_user.user, title=message.text)
        self.tg_client.send_message(tg_user.chat_id, text="Цель создана")
        self.handle_goals_command(tg_user, message)
        self.client.pop(tg_user.chat_id, None)

    def handle_available_list_commands(self, tg_user: TgUser,  message: Message, template: str):
        if message.text.startswith('/') and message.text.startswith('/') not in COMMANDS:
            text = render_template(template)
            self.tg_client.send_message(chat_id=tg_user.chat_id, text=text)
        else:
            text = render_template(template)
            self.tg_client.send_message(chat_id=tg_user.chat_id, text=text)

