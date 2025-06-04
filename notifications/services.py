import requests
from django.conf import settings


class TelegramNotificationService:
    BASE_URL = "https://api.telegram.org/bot{token}/sendMessage"

    @classmethod
    def send_notification(cls, message: str) -> bool:
        token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID

        if not token or not chat_id:
            return False

        url = cls.BASE_URL.format(token=token)
        payload = {
            "chat_id": chat_id,
            "text": message,
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException:
            return False
