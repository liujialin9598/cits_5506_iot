from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
import json



def index(request):
    return HttpResponse("Hello, world. You're at the iot index.")



@csrf_exempt  # 暂时禁用CSRF（生产中应启用适当的安全措施）
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ph = data.get('ph')
            tds = data.get('tds')

            # 保存数据到数据库
            SensorData.objects.create(ph=ph, tds=tds)

            return JsonResponse({'status': 'success', 'message': 'Data received'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def get_sensor_data(request):
    try:
        # 获取所有数据并按照时间戳降序排列（最近的数据在前）
        data = SensorData.objects.all().order_by('-timestamp')
        
        # 构造返回的JSON数据
        response_data = []
        for entry in data:
            response_data.append({
                'ph': entry.ph,
                'tds': entry.tds,
                'timestamp': entry.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            })

        return JsonResponse({'status': 'success', 'data': response_data}, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
