from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData, StatusData
import json


def index(request):
    return HttpResponse("Hello, world. You're at the iot index.")


@csrf_exempt  # 暂时禁用CSRF（生产中应启用适当的安全措施）
def receive_data(request):
    if request.method == "POST":
        try:
            print(request.body)
            data = json.loads(request.body)
            ph = data.get("ph")

            tds = data.get("tds")
            temp = data.get("tmp")

            # 保存数据到数据库
            SensorData.objects.create(ph=ph, tds=tds, tmp=temp)
            refresh = StatusData.objects.first()

            return JsonResponse({"status": "success", "message": "Data received","refreshing":refresh.refreshing})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})


def get_sensor_data(request):
    try:
        # 获取所有数据并按照时间戳降序排列（最近的数据在前）
        data = SensorData.objects.all().order_by("-timestamp")[:40]

        # 构造返回的JSON数据
        response_data = []
        for entry in data:
            response_data.append(
                {
                    "ph": entry.ph,
                    "tds": entry.tds,
                    "tmp": entry.tmp,
                    "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
        return JsonResponse({"status": "success", "data": response_data}, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@csrf_exempt  # 暂时禁用CSRF（生产中应启用适当的安全措施）
def refresh(request):
    if request.method == "POST":
        try:
            refresh = StatusData.objects.first()
            if refresh is not None:
                # 将 refreshing 字段设置为 True
                refresh.refreshing = True
                # 保存更改
                refresh.save()
            else:
                # 如果没有实例，可以创建一个新的 StatusData 实例
                refresh = StatusData(refreshing=True)
                refresh.save()
            return JsonResponse({"status": "success", "message":refresh.refreshing})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt  # 暂时禁用CSRF（生产中应启用适当的安全措施）
def fresh_stop(request):
    if request.method == "POST":
        try:
            refresh = StatusData.objects.first()
            if refresh is not None:
                # 将 refreshing 字段设置为 True
                refresh.refreshing = False
                # 保存更改
                refresh.save()
            else:
                # 如果没有实例，可以创建一个新的 StatusData 实例
                refresh = StatusData(refreshing=False)
                refresh.save()
            return JsonResponse({"status": "success", "message":refresh.refreshing})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method"})

