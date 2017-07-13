# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from collab.models import Technology
from collab.models import Project
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    picture = models.ImageField(blank=True, null=True)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=15)
    technologies = models.ManyToManyField(Technology, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    experience = models.TextField(max_length=500, blank=True)
    availability = models.TextField(max_length=500, blank=True)
    skills = TaggableManager(verbose_name='Skills', help_text=('A comma-separated list of skills'))

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.user.username})

    @property
    def pic_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        return '/static/images/default_prof_pic.jpg'

    def __str__(self):
        return unicode(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Request(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return 'From: ' + unicode(self.sender) + ' | ' + unicode(self.project)


# class RequestInline(admin.TabularInline):
#     model = Request
#     extra = 1


class SocialUser(models.Model):
    WEBSITE = 'ps'
    GITHUB = 'gh'
    LINKEDIN = 'li'
    TWITTER = 'tw'
    TRELLO = 'tl'
    FACEBOOK = 'fb'
    PLATFORM_CHOICES = (
        (WEBSITE, 'Website'),
        (GITHUB, 'GitHub'),
        (LINKEDIN, 'LinkedIn'),
        (TWITTER, 'Twitter'),
        (TRELLO, 'Trello'),
        (FACEBOOK, 'Facebook')
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    platform = models.CharField(max_length=2, choices=PLATFORM_CHOICES, default=WEBSITE)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return unicode(self.platform) + ': ' + unicode(self.url)


class SocialInline(admin.TabularInline):
    model = SocialUser
    extra = 1
