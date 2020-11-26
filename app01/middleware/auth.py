# -*- coding: utf-8 -*-


from django.utils.deprecation import MiddlewareMixin
from app01 import models
from django.shortcuts import redirect
from django.conf import settings


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # request.tracer = Tracer()
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer = user_object

        # 白名单 没有登陆都可以访问的页面
        # 获取url,是否在白名单中，不在返回登陆
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        if not request.tracer:
            return redirect('app01:login')
