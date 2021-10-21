from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User
from collab.models import Technology
from collab.models import Project
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=254)
    pronouns = models.CharField(max_length=254, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=254)
    picture = models.ImageField(blank=True, null=True)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=15, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    experience = models.TextField(max_length=500, blank=True)
    availability = models.TextField(max_length=500, blank=True)
    skills = TaggableManager(verbose_name='Skills', help_text='A comma-separated list of skills')

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.user.username})

    @property
    def pic_url(self):
        if self.picture and hasattr(self.picture, 'url'):
            return self.picture.url
        return '/static/images/default_prof_pic.jpg'

    def __str__(self):
        return str(self.user.username)


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
    date = models.DateTimeField("Date", default=timezone.now)

    def __str__(self):
        return 'From: ' + str(self.sender) + ' | ' + str(self.project)


# class RequestInline(admin.TabularInline):
#     model = Request
#     extra = 1


class SocialUser(models.Model):
    WEBSITE = '/static/images/website.png'
    GITHUB = '/static/images/github.png'
    LINKEDIN = '/static/images/linkedin.png'
    TWITTER = '/static/images/twitter.png'
    FACEBOOK = '/static/images/facebook.png'
    INSTAGRAM = '/static/images/instagram.png'
    PLATFORM_CHOICES = (
        (WEBSITE, 'Website'),
        (GITHUB, 'GitHub'),
        (LINKEDIN, 'LinkedIn'),
        (TWITTER, 'Twitter'),
        (FACEBOOK, 'Facebook'),
        (INSTAGRAM, 'Instagram'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    platform = models.CharField(max_length=100, choices=PLATFORM_CHOICES, default=WEBSITE)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.platform) + ': ' + str(self.url)


class SocialInline(admin.TabularInline):
    model = SocialUser
    extra = 1
