# -*- coding: utf-8 -*-


from django.utils.deprecation import MiddlewareMixin
from app01 import models
from django.shortcuts import redirect
from django.conf import settings
import datetime
from django.core.urlresolvers import resolve


# 封装处理
class Tracer(object):

    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.tracer = Tracer()
        user_id = request.session.get('user_id', 0)
        user_object = models.UserInfo.objects.filter(id=user_id).first()
        request.tracer.user = user_object

        # 白名单 没有登陆都可以访问的页面
        # 获取url,是否在白名单中，不在返回登陆
        if request.path_info in settings.WHITE_REGEX_URL_LIST:
            return

        if not request.tracer.user:
            return redirect('app01:login')

        # 登陆成功之后，已登陆，获取当前用户的所有的额度

        # 方式一： 免费的额度在交易记录表中存储

        # 获取当前用户ID值最大（最近交易记录）
        _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).order_by('-id').first()

        # 判断是否过期
        current_datatime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datatime:
            _object = models.Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()

        request.tracer.price_policy = _object.price_policy

        # 方式二
        # 获取当前用户ID值最大（最近交易记录）
        """
        _object = models.Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()

        if not _object:
            # 没有购买
            request.tracer.price_policy = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        else:
            # 付费版
            current_datetime = datetime.datetime.now()
            if _object.end_datetime and _object.end_datetime < current_datetime:
                request.tracer.price_policy = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
            else:
                request.tracer.price_policy = _object.price_policy
        """

    def process_view(self, request, view, args, kwargs):
        if not request.path_info.startswith('/app01/manage/'):
            return

        project_id = kwargs.get('project_id')
        project_object = models.Project.objects.filter(creator=request.tracer.user, id=project_id).first()
        if project_object:
            request.tracer.project = project_object
            return

        project_user_object = models.ProjectUser.objects.filter(user=request.tracer.user, project_id=project_id).first()
        if project_user_object:
            # 是我参与的项目
            request.tracer.project = project_user_object.project
            return

        return redirect('app01:project_list')
