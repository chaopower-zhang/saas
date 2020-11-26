from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.forms.account import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from django.urls import reverse
from utils.image_code import check_code
from io import BytesIO
from app01 import models
import uuid
import datetime
from django.db.models import Q


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
        # form.save()
        instance = form.save()

        # 创建交易记录
        policy_object = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )
        return JsonResponse({'status': True, 'data': reverse('app01:login')})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'login_sms.html', {'form': form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        mobile_phone = form.cleaned_data['mobile_phone']
        user_object = models.UserInfo.objects.filter(mobile_phone=mobile_phone).first()
        request.session['user_id'] = user_object.id
        return JsonResponse({'status': True, 'data': 'app01:project_list'})
    else:
        return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_object = models.UserInfo.objects.filter(
            Q(username=username) | Q(email=username)).filter(password=password).first()
        if user_object:
            request.session['user_id'] = user_object.id
            request.session.set_expiry(60 * 60 * 24 * 14)

            return redirect('app01:project_list')

        form.add_error('username', '用户名或密码错误')
    return render(request, 'login.html', {'form': form})


def image_code(request):
    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s

    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('app01:project_list')
