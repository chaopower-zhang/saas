from django.conf.urls import url, include
from app01.views import account

urlpatterns = [
    url(r'^register/$', account.register, name='register'),
    url(r'^login/$', account.login, name='login'),
    url(r'^send_sms/$', account.send_sms, name='send_sms'),
]