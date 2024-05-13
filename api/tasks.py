from api.utils.mqtt_server import MQTTClient
from celery import shared_task
from django.conf import settings

client = MQTTClient()


@shared_task
def send_mqtt_heart_beat():
    client.publish("/health", {"message": "Hello World"})
