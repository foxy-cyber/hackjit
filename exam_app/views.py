from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Student, Administrator,User
from exam_app.cv.Code.updated_cv import first_function

def home(request):
    return render(request, 'home.html')

def webcam(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        if Student.objects.filter(usn=usn).exists():
            return render(request, 'webcam.html',{'usn': usn})
        else:
            return render(request, 'home.html', {'error': 'Invalid USN'})
    return render(request, 'home.html')

def admin_login(request):
    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        password = request.POST.get('password')
        try:
            admin = Administrator.objects.get(admin_id=admin_id)
            if admin.user.password==password:
                return redirect('admin_dashboard')
            else:
                return render(request, 'admin_login.html', {'error': 'wrong password'})
        except Administrator.DoesNotExist:
            return render(request, 'admin_login.html', {'error': 'Invalid admin ID or password'})
    return render(request, 'admin_login.html')

def admin_dashboard(request):
    students = Student.objects.all()  # Retrieve all students from the database
    return render(request, 'admin_dashboard.html', {'students': students})

from django.http import JsonResponse

# exam_app/views.py

import base64
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def video_stream(request):
    if request.method == 'POST':
        usn = request.POST.get('usn')
        SAVE_DIR = 'C:/Users/tilak/Desktop/hackathon/exam_project/exam_app/cv/Code/images/'

        if usn:
            save_dir = os.path.join(SAVE_DIR, usn)  # Creating directory path with usn
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            frame = request.FILES.get('frame')  # Retrieve the frame data from form data
            if frame:
                # Save the frame to a file
                frame_name = os.path.join(save_dir, 'frame{}.png'.format(len(os.listdir(save_dir))))
                with open(frame_name, 'wb') as f:
                    for chunk in frame.chunks():
                        f.write(chunk)

                # Send a response
                return JsonResponse({'message': 'Frame saved successfully'}, status=200)
            else:
                return JsonResponse({'error': 'No frame data received'}, status=400)
        else:
            return JsonResponse({'error': 'No USN provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


def run_cv(request):
    if request.method == 'GET':
        usn = request.GET.get('usn')
        print("running")
        score = first_function(usn)
        print("done")
        score = int(score)
        return JsonResponse({'score': score})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
    
    
