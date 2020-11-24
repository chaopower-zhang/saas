from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from django.urls import reverse
from utils.image_code import check_code
from io import BytesIO


# Create your views here.


def send_sms(request):
    form = SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'resgister.html', {'form': form})
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': reverse('app01:login_sms')})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        return JsonResponse({'status': True, 'data': '/index/'})
    else:
        return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        # return JsonResponse({'status': True, 'data': '/index/'})
        return redirect('/index/')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s

    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())
