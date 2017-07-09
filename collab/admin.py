# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Technology, Project, CollabInline, MatchInline


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    filter_horizontal = ('technologies',)
    inlines = (CollabInline, MatchInline,)


class UserAdmin(admin.ModelAdmin):
    inlines = (CollabInline, MatchInline,)


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


# class CollabAdmin(admin.ModelAdmin):
#     list_display = ('user',)
#     search_fields = ['user']
#
#
# class MatchAdmin(admin.ModelAdmin):
#     list_display = ('user',)
#     search_fields = ['user']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Technology, TechnologyAdmin)
# admin.site.register(Collab, CollabAdmin)
# admin.site.register(Match, MatchAdmin)
