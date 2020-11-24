from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from app01.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm
from django.urls import reverse
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
        return JsonResponse({'status': True, 'data': reverse('app01:login')})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login.html', {'form':form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        return JsonResponse({'status': True, 'data':'/index/'})
    else:
        return JsonResponse({'status': False, 'error': form.errors})
