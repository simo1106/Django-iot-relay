import os
import sys
import django
import json
import paho.mqtt.client as mqtt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot_relay.settings")
django.setup()

from myapp.models import RelayState, RelayLog
from mqtt_config import (
    MQTT_SERVER,
    MQTT_PORT,
    MQTT_USERNAME,
    MQTT_PASSWORD,
    MQTT_TOPIC_CONTROL,
    MQTT_TOPIC_STATUS,
)


def save_log(data, source, topic):
    RelayLog.objects.create(
        relay1=data.get("relay1", "off"),
        relay2=data.get("relay2", "off"),
        relay3=data.get("relay3", "off"),
        relay4=data.get("relay4", "off"),
        source=source,
        topic=topic,
    )

    count = RelayLog.objects.count()
    if count > 1000:
        old_logs = RelayLog.objects.order_by("created_at")[:count - 1000]
        RelayLog.objects.filter(id__in=[log.id for log in old_logs]).delete()


def update_state(data):
    state, created = RelayState.objects.get_or_create(id=1)

    state.relay1 = data.get("relay1", state.relay1)
    state.relay2 = data.get("relay2", state.relay2)
    state.relay3 = data.get("relay3", state.relay3)
    state.relay4 = data.get("relay4", state.relay4)

    state.save()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT connected")
        client.subscribe(MQTT_TOPIC_STATUS)
        client.subscribe(MQTT_TOPIC_CONTROL)
        print("Subscribed:", MQTT_TOPIC_STATUS)
        print("Subscribed:", MQTT_TOPIC_CONTROL)
    else:
        print("MQTT connect failed:", rc)


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print("Receive:", msg.topic, data)

        update_state(data)

        if msg.topic == MQTT_TOPIC_CONTROL:
            save_log(data, "mqtt", MQTT_TOPIC_CONTROL)
        elif msg.topic == MQTT_TOPIC_STATUS:
            # 狀態回報只更新畫面狀態，不一定要記錄
            pass

    except Exception as e:
        print("MQTT message error:", e)


client = mqtt.Client()
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_SERVER, MQTT_PORT, 60)
client.loop_forever()