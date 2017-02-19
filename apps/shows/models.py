#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    apps.shows.models
    ~~~~~~~~~~~~~~~

    Rss system models. Including RSS sources and RSS news.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import datetime

from django.db import models


class BzSource(models.Model):

    class Meta:
        db_table = "bz_source"

    title = models.CharField(max_length=128, unique=True)
    url = models.CharField(max_length=256, unique=True)

    # Source type. default is RSS
    # Maybe it's will support more source like WEB spiders in the future.
    # 1: RSS
    source_type = models.SmallIntegerField(default=1)

    # the frequency of the source's refresh.
    # default 30 min.
    refresh_freq = models.IntegerField(default=30)
    last_refresh_time = models.DateTimeField(default=datetime.datetime.now)
    author = models.CharField(max_length=64, unique=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzSource - {title}>".format(title=self.title)

    def update_last_refresh_time(self, refresh_time):
        self.last_refresh_time = refresh_time


class BzArticles(models.Model):

    class Meta:
        db_table = "bz_articles"

    title = models.CharField(max_length=512, unique=True)
    url = models.CharField(max_length=256)
    summary = models.CharField(max_length=512, default="")
    contents = models.TextField()
    likes = models.IntegerField(default=0)
    source = models.ForeignKey(BzSource, on_delete=models.CASCADE)

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<BzArticle {title} - {likes}>".format(
            title=self.title, likes=self.likes,
        )

    def like(self):
        self.likes += 1

    def unlike(self):
        self.likes -= 1


class BzLikeLog(models.Model):

    class Meta:
        db_table = "bz_like_log"

    article_id = models.BigIntegerField(db_index=True)
    user_id = models.BigIntegerField(db_index=True)

    # like or unlike
    # 1: like
    # 2: unlike
    operate = models.SmallIntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_operate(self):
        if self.operate == 1:
            return "like"
        elif self.operate == 2:
            return "unlike"
        else:
            return "unknown"

    def __str__(self):
        return "<BzLikeLog {aid} - {op}>".format(
            aid=self.article_id, op=self.get_operate()
        )
