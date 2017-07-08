# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Technology, Project, Request, Collab, Match


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    filter_horizontal = ('technologies',)


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Request)
admin.site.register(Collab)
admin.site.register(Match)
