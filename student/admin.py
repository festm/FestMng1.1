# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Fuser,Request,Brmsg,QCM,Oversee

# Register your models here.
admin.site.register(Fuser)
admin.site.register(Request)
admin.site.register(Brmsg)
admin.site.register(QCM)
admin.site.register(Oversee)

