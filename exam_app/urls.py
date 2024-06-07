from django.urls import path
from .views import home, webcam, admin_login, admin_dashboard,video_stream,run_cv

urlpatterns = [
    path('', home, name='home'),
    path('webcam/', webcam, name='webcam'),
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('video_stream/',video_stream,name='video_stream'),
    path('run_cv/', run_cv, name='run_cv'),
]
