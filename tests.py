#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author: Gao Shao Yang


from django.core.cache import cache



cache.set("a", "gao", 10)


print(cache.get("a"))