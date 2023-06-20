
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient
from bot.tg.render import render_template


class VerificationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        serializer = TgUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_user = serializer.save(user=request.user)
        text = render_template("successful_validation.j2")
        TgClient().send_message(chat_id=tg_user.chat_id, text=text)
        return Response(serializer.data)
