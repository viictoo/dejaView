from django.db import models
from django.contrib.auth.models import AbstractUser, User
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    """Model representing user profiles.

    Args:
        models (module): The Django models module.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model,
            specifying the user associated with the profile.
        phone_number (PhoneNumberField): A phone number field allowing blank
            and null values, with optional help text.
        image (ImageField): An image field with a default image and a
            specified upload path for profile pictures.

    Returns:
        str: A string repr of the class, showing the associated username.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        blank=True, null=True, help_text=u"Phone Number...")
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # image compression using PIL disabled for AWS storage

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     img = Image.open(self.image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         print(vars(self.image))
    #         img.save(self.image.path)
