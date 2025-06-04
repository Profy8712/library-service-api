from celery import shared_task
from notifications.services import TelegramNotificationService


@shared_task
def send_telegram_notification(message: str) -> None:
    TelegramNotificationService.send_notification(message)
