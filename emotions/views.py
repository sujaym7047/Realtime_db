from django.shortcuts import render
from django.http import JsonResponse
from .models import EmotionLog
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

def get_latest_emotions(request):
    emotions = EmotionLog.objects.order_by('-time')[:20]  # Get latest 20
    data = [{"time": e.time.strftime("%Y-%m-%d %H:%M:%S"), "emotion": e.emotion} for e in emotions]
    return JsonResponse(data, safe=False)

def dashboard(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def record_emotion(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            emotion = body.get("emotion")
            if emotion:
                EmotionLog.objects.create(emotion=emotion, time=timezone.now())
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "No emotion provided"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

