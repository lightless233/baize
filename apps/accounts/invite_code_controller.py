#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.accounts.invite_code_controller
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Invite Code manage controller.
    Just for admin.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.views import View
from django.conf import settings
from django.http import JsonResponse

from apps.accounts.models import BzActiveCode
from utils import make_random_string


class MakeInviteCodeView(View):

    @staticmethod
    def get(request):
        token = request.GET.get("token", "")
        if token != settings.IC_TOKEN:
            return JsonResponse(dict(code=666, message="Hacker! Fuck You!"))
        num = request.GET.get("num", 1)
        code_length = request.GET.get("length", 16)

        ic_list = list()
        for x in range(int(num)):
            new_ic = BzActiveCode()
            new_ic.user_id = 0
            new_ic.code = make_random_string(code_length)
            ic_list.append(new_ic.code)
            new_ic.save()
        return JsonResponse(dict(code=1001, message="success", ic_list=ic_list))




