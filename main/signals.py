from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import UserProfile

#when an user object is created this picks up the signal, if created then we create user profile 
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		userprofile = UserProfile.objects.create(user=instance)
