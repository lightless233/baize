#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.accounts.models
    ~~~~~~~~~~~~~~~~~~~~

    Accounts system models

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

from django.db import models


class BzUser(models.Model):
    """
    Store user's basic information.
    """

    class Meta:
        db_table = "bz_user"

    username = models.CharField(max_length=32, null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=256, null=False, blank=False)
    token = models.CharField(max_length=32, null=False, blank=False, unique=True)

    # 1: not active, 2: normal user, 3: banned user
    status = models.PositiveSmallIntegerField(default=1, blank=False, null=False, db_index=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class BzUserLoginLog(models.Model):
    """
    Store user's login log.
    Include IP and Time
    """

    class Meta:
        db_table = "bz_user_login_log"

    ip = models.CharField(max_length=16, null=False, blank=True, default="0.0.0.0")
    login_time = models.DateTimeField(null=False, blank=True, default="")

    user = models.ForeignKey(BzUser, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)


class BzActiveCode(models.Model):
    """
    Store all active code, or invite code.
    """

    class Meta:
        db_table = "bz_active_code"


