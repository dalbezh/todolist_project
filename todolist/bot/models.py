from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TgUser(models.Model):
    """
    user = models.OneToOneField -->
    у одного User может быть один tg_id
    """
    chat_id = models.PositiveBigIntegerField(primary_key=True, editable=False, unique=True, verbose_name="ID Чата")
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    verification_code = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.__class__.__str__()} {self.chat_id}'

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"
