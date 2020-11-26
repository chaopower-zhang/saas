from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.core.exceptions import ValidationError
import random
from utils.tencent.sms import send_sms_single
from utils.encrypt import md5
from django_redis import get_redis_connection
from app01.forms.bootstrap import BootStrapForm


class RegisterModelForm(BootStrapForm, forms.ModelForm):

    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput())

    mobile_phone = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    def clean_username(self):
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')
            # self.add_error('username','用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm_pwd = md5(self.cleaned_data['confirm_password'])

        if pwd != confirm_pwd:
            raise ValidationError('两次密码不一致')
        return confirm_pwd

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']

        # mobile_phone = self.cleaned_data['mobile_phone']
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile_phone', 'code']


class SendSmsForm(forms.Form):
    mobile_phone = forms.CharField(
        label='手机号', validators=[RegexValidator(r'^1[3|4|5|6|7|8|9]\d{9}$', '手机格式错误'), ]
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError('短信模板错误')

        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if tpl == 'login':
            if not exists:
                raise ValidationError('手机号不存在')
        else:
            if exists:
                raise ValidationError('手机号已存在')

        code = random.randrange(1000, 9999)
        sms = send_sms_single(mobile_phone, template_id, [code, ])
        if sms['result'] != 0:
            raise ValidationError('短信发送失败，{}'.format(sms['errmsg']))

        # 验证码写入redis
        conn = get_redis_connection()
        conn.set(mobile_phone, code, ex=60)
        return mobile_phone


class LoginSMSForm(BootStrapForm, forms.Form):
    mobile_phone = forms.CharField(
        label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput())

    def clean_mobile_phone(self):
        mobile_phone = self.cleaned_data['mobile_phone']
        exists = models.UserInfo.objects.filter(mobile_phone=mobile_phone).exists()
        if not exists:
            raise ValidationError('手机号未注册')
        return mobile_phone

    def clean_code(self):
        code = self.cleaned_data['code']

        # mobile_phone = self.cleaned_data['mobile_phone']
        mobile_phone = self.cleaned_data.get('mobile_phone')
        if not mobile_phone:
            return code

        conn = get_redis_connection()
        redis_code = conn.get(mobile_phone)
        if not redis_code:
            raise ValidationError('验证码失效或未发送，请重新发送')

        redis_str_code = redis_code.decode('utf-8')

        if code.strip() != redis_str_code:
            raise ValidationError('验证码错误，请重新输入')

        return code


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='用户名或邮箱')
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    code = forms.CharField(label='图片验证码', widget=forms.TextInput())

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = self.cleaned_data['password']
        # 加密 & 返回
        return md5(pwd)

    def clean_code(self):
        """ 钩子 图片验证码是否正确？ """
        # 读取用户输入的yanzhengm
        code = self.cleaned_data['code']

        # 去session获取自己的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        if code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')

        return code
