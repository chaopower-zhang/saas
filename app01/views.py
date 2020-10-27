from django.shortcuts import render, HttpResponse
import random
from utils.tencent.sms import send_sms_single

# Create your views here.

def send_sms(request):
    code = random.randrange(1000, 9999)
    res = send_sms_single('16628532878', 758311, [code, ])
    print(res)
    return HttpResponse('成功')
