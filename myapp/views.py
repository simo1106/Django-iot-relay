from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import RelayState, RelayLog
from .mqtt_client import publish_relay_control
from mqtt_config import MQTT_TOPIC_CONTROL


def get_state():
    state, created = RelayState.objects.get_or_create(id=1)
    return state


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


def index(request):
    return render(request, "myapp/index.html")


def logs_page(request):
    logs = RelayLog.objects.all()[:1000]
    return render(request, "myapp/logs.html", {"logs": logs})


def api_state(request):
    state = get_state()
    return JsonResponse({
        "relay1": state.relay1,
        "relay2": state.relay2,
        "relay3": state.relay3,
        "relay4": state.relay4,
    })


@csrf_exempt
def api_control(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    data = json.loads(request.body.decode("utf-8"))
    state = get_state()
    state.relay1 = data.get("relay1", state.relay1)
    state.relay2 = data.get("relay2", state.relay2)
    state.relay3 = data.get("relay3", state.relay3)
    state.relay4 = data.get("relay4", state.relay4)
    print("now:", state.relay1, state.relay2, state.relay3, state.relay4)
    state.save()

    save_log(data, "web", MQTT_TOPIC_CONTROL)

    publish_relay_control(data)

    return JsonResponse({
        "message": "relay control published",
        "data": data
    })


def api_logs(request):
    logs = RelayLog.objects.all()[:1000]

    result = []
    for log in logs:
        result.append({
            "relay1": log.relay1,
            "relay2": log.relay2,
            "relay3": log.relay3,
            "relay4": log.relay4,
            "source": log.source,
            "topic": log.topic,
            "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    return JsonResponse(result, safe=False)