# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Technology, Project, Platform, Social, Request, Collab, Match

# Register your models here.

admin.site.register(Technology)
admin.site.register(Project)
admin.site.register(Platform)
admin.site.register(Social)
admin.site.register(Request)
admin.site.register(Collab)
admin.site.register(Match)
