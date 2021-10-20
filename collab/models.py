from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime
from taggit.managers import TaggableManager
from django.utils import timezone


class Technology(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=500)
    founder = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("Date", default=timezone.now)
    description = models.TextField(blank=True, max_length=1000)
    city = models.CharField(max_length=50)
    technologies = models.ManyToManyField(Technology)
    archived = models.BooleanField(verbose_name='Archive', default=False)
    matches = models.ManyToManyField(User, through='Match', related_name='matches')
    collaborators = models.ManyToManyField(User, through='Collab', related_name='collaborators')
    skills_needed = TaggableManager(verbose_name="Skills Needed", help_text="A comma-separated list of skills")

    def get_absolute_url(self):
        return reverse('collab:project', kwargs={'pk': self.pk})

    def __str__(self):
        return "" + self.title + ' - ' + str(self.founder)


class Collab(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class CollabInline(admin.TabularInline):
    model = Collab
    extra = 1


class Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.project)


class MatchInline(admin.TabularInline):
    model = Match
    extra = 1


class SocialProj(models.Model):
    WEBSITE = 'ps'
    GITHUB = 'gh'
    LINKEDIN = 'li'
    TWITTER = 'tw'
    TRELLO = 'tl'
    FACEBOOK = 'fb'
    INSTAGRAM = 'ig'
    YOUTUBE = 'yt'
    PLATFORM_CHOICES = (
        (WEBSITE, 'fa fa-globe fa-3x'),
        (GITHUB, 'fa fa-github fa-3x'),
        (LINKEDIN, 'fa fa-linkedin fa-3x'),
        (TWITTER, 'fa fa-twitter fa-3x'),
        (TRELLO, 'fa fa-trello fa-3x'),
        (FACEBOOK, 'fa fa-facebook-square fa-3x'),
        (INSTAGRAM, 'fa fa-instagram fa-3x'),
        (YOUTUBE, 'fa fa-youtube fa-3x')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES, default=GITHUB)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.platform) + ': ' + str(self.url)


class SocialInline(admin.TabularInline):
    model = SocialProj
    extra = 1

