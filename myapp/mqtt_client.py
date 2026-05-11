import json
import paho.mqtt.client as mqtt
from mqtt_config import (
    MQTT_SERVER,
    MQTT_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
    MQTT_TOPIC_CONTROL,
)


def publish_relay_control(data):
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_SERVER, MQTT_PORT, 60)

    payload = json.dumps(data)
    client.publish(MQTT_TOPIC_CONTROL, payload)

    client.disconnect()