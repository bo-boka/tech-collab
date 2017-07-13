# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from accounts.models import SocialInline, Request, UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ['user']
    filter_horizontal = ('technologies',)
    inlines = (SocialInline,)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Request)
