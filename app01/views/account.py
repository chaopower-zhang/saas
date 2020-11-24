from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from app01.forms.account import RegisterModelForm, SendSmsForm

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
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})