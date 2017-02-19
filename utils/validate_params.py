#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    utils.validate_params
    ~~~~~~~~~~~~~~~~~~~~~

    check if params is validate.

    :author:    lightless <root@lightless.me>
    :homepage:  https://github.com/LiGhT1EsS/baize
    :license:   GPL-3.0, see LICENSE for more details.
    :copyright: Copyright (c) 2017 lightless. All rights reserved
"""


class DataDict(object):
    """
    Data dict.
    You can get/set value via dot.
    >>> dd = DataDict()
    >>> dd.key1 = "value1"
    >>> print(dd.key1)
    value1
    >>> print(dd.key2)
    None
    """

    inner_dict = dict()

    def __set__(self, instance, value):
        DataDict.inner_dict[instance] = value

    def __getattr__(self, item):
        return DataDict.inner_dict.get(item, None)


class ValidateParams(object):
    """
    check if the params is empty.
    """

    def __init__(self, all_params, must_have_params=None):
        super(ValidateParams, self).__init__()
        if must_have_params is None:
            self._params = list()
        else:
            self._params = must_have_params
        self.args = DataDict()
        self.error_message = None
        self._all_params = all_params

    def check(self):
        """
        really check function.
        :return: Boolean
        """
        if not isinstance(self._params, list):
            self.error_message = "No list found."
            return False
        for k, v in self._all_params.items():

            setattr(self.args, k, v)

            if k in self._params:
                if v == "" or v is None:
                    self.error_message = "参数[{0}]不能为空".format(k)
                    return False
        return True
