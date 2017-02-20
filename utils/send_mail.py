#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils.send_mail
    ~~~~~~~~~~~~~~~

    Send email package.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import threading

from django.core.mail import send_mail as django_send_mail


def send_mail(subject, content, sender, to, **kwargs):

    async_flag = kwargs.pop("async_flag", True)
    fail_silently = kwargs.pop("fail_silently", False)

    if async_flag:
        payload = {
            "subject": subject,
            "message": content,
            "from_email": sender,
            "recipient_list": to,
            "fail_silently": fail_silently
        }
        t = threading.Thread(target=django_send_mail, name="send_mail", kwargs=payload)
        t.start()
    else:
        django_send_mail(subject, content, sender, to, fail_silently=fail_silently)

