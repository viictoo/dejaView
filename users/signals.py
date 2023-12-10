from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Creates a user profile when a new user is created.

    Args:
        sender (signal): The signal for user creation.
        instance (object): The user object created.
        created (bool): A flag indicating whether the user is newly created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Saves user profile information when a user is created or updated.

    Args:
        sender (signal): The model object that is the source of the signal.
        instance (object): The user object.
    """
    instance.profile.save()
