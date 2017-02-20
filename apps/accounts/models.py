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

import datetime

from django.db import models
from django.contrib.auth.hashers import make_password, check_password


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

    # user status
    # 1: not active, 2: normal user, 3: banned user
    status = models.PositiveSmallIntegerField(default=1, blank=False, null=False, db_index=True)

    # user's role
    # 1: guest: can only view all news.
    # 2: member: can like or unlike the news.
    # 3: shows manager: can view admin panel. can add/del/edit shows source or import opml file.
    # 4-9: Reserved.
    # 10: master: can do anything.
    role = models.PositiveSmallIntegerField(default=1, blank=False, null=False)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzUser {user_id} - {username} - {status} - {role}>".format(
            user_id=self.id, username=self.username, status=self.get_status(),
            role=self.role
        )

    def get_status(self):
        """
        get user status by status code.
        :return: unicode
        """
        status_dict = {
            1: "未激活",
            2: "正常",
            3: "禁止登陆",
        }
        try:
            return status_dict[self.status]
        except KeyError:
            return "未知状态"

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)


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

    def __str__(self):
        return "<BzUserLoginLog {username} - {ip} - {login_time}>".format(
            username=self.user.username,
            ip=self.ip,
            login_time=self.login_time.strftime("%Y-%m-%d %H:%M:%S")
        )


class BzActiveCode(models.Model):
    """
    Store all active code, or invite code.
    """

    class Meta:
        db_table = "bz_active_code"

    user_id = models.BigIntegerField(null=False, blank=False, default=0)
    code = models.CharField(max_length=32, null=False, blank=True, default="")
    used_time = models.DateTimeField(auto_now_add=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def use_code(self, user_id=None):
        """
        Use this active code for user_id
        :param user_id: Integer
        :return: Boolean
        """
        if user_id:
            self.user_id = user_id
            self.used_time = datetime.datetime.now()
            return True
        else:
            return False

    def __str__(self):
        return "<BzActiveCode {code} - {status}>".format(
            code=self.code, status=self.get_status()
        )

    def get_status(self):
        """
        Get if this code already be used.
        :return: unicode
        """
        if self.user_id == 0:
            return "未使用"
        else:
            return "已使用"


