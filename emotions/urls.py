from django.urls import path
from . import views

urlpatterns = [
    path('',views.dashboard),
    path('api/emotions/', views.get_latest_emotions, name='get_latest_emotions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/record_emotion/', views.record_emotion, name='record_emotion'),
]
