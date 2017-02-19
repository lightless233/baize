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

from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse

from utils import logger, ValidateParams


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



