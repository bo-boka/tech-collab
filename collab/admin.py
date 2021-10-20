# from __future__ import unicode_literals

from django.contrib import admin
from collab.models import Technology, Project, Collab, Match, CollabInline, MatchInline, SocialInline


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title']
    filter_horizontal = ('technologies',)
    inlines = (CollabInline, MatchInline, SocialInline,)


class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Collab)
admin.site.register(Match)
