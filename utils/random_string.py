#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils.random_string
    ~~~~~~~~~~~~~~~~~~~

    make random string.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""

import string
import random


def make_random_string(length=16):
    """
    generate a random string.
    :param length: Integer
    :return: String.
    """
    pool = string.ascii_letters + string.digits
    return "".join([random.choice(pool) for i in range(length)])


if __name__ == '__main__':
    print(make_random_string(16))
