#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.accounts.accounts_controller
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Accounts main controller.
    Including login/register etc.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import binascii
import datetime
import base64
import hashlib
import traceback

from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse

from utils import logger, ValidateParams, make_random_string
from utils.send_mail import send_mail
from apps.accounts.models import BzUser, BzActiveCode


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):

    @staticmethod
    def get(request):
        return render(request, "accounts/login.html")

    @staticmethod
    def post(request):
        params = request.POST
        va = ValidateParams(params, ["email", "password"])
        if not va.check():
            return JsonResponse(dict(code=1004, message=va.error_message))
        # todo: finish login part.


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    """
    注册视图
    """

    @staticmethod
    def get(request):
        return render(request, "accounts/register.html")

    @staticmethod
    def post(request):
        params = request.POST
        vp = ValidateParams(params, ["email", "password", "ic", "username"])
        if not vp.check():
            return JsonResponse(dict(code=1004, message=vp.error_message))

        # 检查invite code是否可用
        invite_code = vp.args.ic
        invite_code_qs = BzActiveCode.objects.filter(user_id=0, code=invite_code).first()
        if not invite_code_qs:
            return JsonResponse(dict(code=1004, message="邀请码无效!"))

        # 检查用户名或邮箱是否被注册
        qs = BzUser.objects.filter(Q(username=vp.args.username) | Q(email=vp.args.email)).first()
        if qs:
            return JsonResponse(dict(code=1004, message="用户名或邮箱已被注册!"))

        # 检查用户名和邮箱是否合法
        if "|" in vp.args.username or "|" in vp.args.email:
            return JsonResponse(dict(code=1004, message="用户名或邮箱中含有非法字符"))

        # 插入用户数据
        new_user = BzUser()
        new_user.username = vp.args.username
        new_user.email = vp.args.email
        new_user.token = make_random_string(32)
        new_user.status = 1
        new_user.role = 1
        new_user.set_password(vp.args.password)
        new_user.save()
        # 更新邀请码的user_id
        invite_code_qs.user_id = new_user.id
        invite_code_qs.used_time = datetime.datetime.now()
        invite_code_qs.save()

        # 发送邮件
        raw_info = "".join(["{0}".format(new_user.id), "|", new_user.email])
        info = base64.b32encode(raw_info.encode("ascii")).decode("utf-8")
        raw_sign = "".join([new_user.token, new_user.username, new_user.email])
        sign = hashlib.md5(raw_sign.encode("ascii")).hexdigest()
        active_link = request.build_absolute_uri(reverse("validate_email")) + "?info={info}&sign={sign}"
        active_link = active_link.format(info=info, sign=sign)
        logger.debug(active_link)
        send_mail(
            "[白泽] 请激活您的白泽账户",
            "您的激活链接为: {url}".format(url=active_link),
            'baize.support@vidar.club',
            [vp.args.email],
            fail_silently=False,
            async_flag=True,
        )

        # 返回成功信息
        return JsonResponse(dict(code=1001, message="注册成功，请到邮箱激活您的账户."))


class ValidateEmailView(View):

    @staticmethod
    def get(request):

        # 获取并验证参数
        params = request.GET
        vp = ValidateParams(params, ["sign", "info"])
        if not vp.check():
            return JsonResponse(dict(code=1004, message=vp.error_message))

        # decode info参数
        try:
            info = base64.b32decode(vp.args.info).decode("utf-8")
        except binascii.Error as e:
            logger.error(e)
            return JsonResponse(dict(code=1004, message="非法的INFO值"))

        # 解包info参数
        try:
            user_id, email = info.split("|")
        except ValueError as e:
            logger.error(e)
            return JsonResponse(dict(code=1004, message="非法的INFO值"))

        # 获取用户信息
        user_qs = BzUser.objects.filter(id=user_id, email=email).first()
        if not user_qs:
            return JsonResponse(dict(code=1004, message="非法的INFO值"))
        if user_qs.status != 1:
            return JsonResponse(dict(code=1004, message="用户已经激活"))

        # 校验sign参数
        raw_sign = "".join([user_qs.token, user_qs.username, user_qs.email])
        if hashlib.md5(raw_sign.encode("ascii")).hexdigest() == vp.args.sign:
            # 更新用户状态
            user_qs.status = 2
            user_qs.save()
            return JsonResponse(dict(code=1001, message="验证成功，现在将自动转入登录页面"))
        else:
            return JsonResponse(dict(code=1004, message="非法的SIGN值"))

