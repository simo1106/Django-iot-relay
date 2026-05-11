import json
import paho.mqtt.client as mqtt
from mqtt_config import (
    MQTT_SERVER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_TOPIC_CONTROL
)

def publish_relay_control(data):
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    
    # 加上 source 標記
    data_with_source = data.copy() 
    data_with_source["source"] = "web" # data_
    
    payload = json.dumps(data_with_source) # 將帶有 source 標記的資料轉換為 JSON 字串
    client.publish(MQTT_TOPIC_CONTROL, payload)
    
    client.disconnect()