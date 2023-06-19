
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        serializer = TgUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_user = serializer.save(user=request.user)

        TgClient().send_message(tg_user.chat_id, 'Bot token verified')

        return Response(serializer.data)
