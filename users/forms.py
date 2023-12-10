from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField


class UserRegisterForm(UserCreationForm):
    """Form for user registration.

    Args:
        UserCreationForm (class): Django's built-in form for user creation.

    Attributes:
        email (EmailField): Field for the user's email.
        phone_number (PhoneNumberField): Field for the user's phone number,
        allows blank values.
    """
    email = forms.EmailField()
    phone_number = PhoneNumberField(required=False)

    class Meta:
        """Metadata for the UserRegisterForm.

        Attributes:
            model (class): The User model.
            fields (list): The fields to include in the form.
        """
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'phone_number'
            ]

    def save(self, commit=True):
        """Save the user and create/update the associated profile.

        Args:
            commit (bool, optional): Whether to commit the changes.
            Default True.

        Returns:
            User: The user object.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        # Create or update the associated profile
        profile, created = Profile.objects.get_or_create(user=user)
        phone_number = self.cleaned_data['phone_number']

        # clean phone number
        phone_number_value = phone_number.raw_input
        if phone_number_value[0] == "+":
            phone_number_value = phone_number_value[1:]
        if phone_number_value[0] == "0":
            phone_number_value = "254" + phone_number_value[1:]

        profile.phone_number = phone_number_value

        if commit:
            profile.save()

        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information.

    Args:
        forms (module): Django forms module.

    Attributes:
        email (EmailField): Field for the user's email address.
    """
    email = forms.EmailField()

    class Meta:
        """Metadata for the UserUpdateForm.

        Attributes:
            model (class): The User model.
            fields (list): The fields to include in the form.
        """
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information.

    Args:
        forms (module): The Django forms module.

    Attributes:
        phone_number (PhoneNumberField): A user's phone number, allows blank.
    """
    phone_number = PhoneNumberField(required=False)

    class Meta:
        """Metadata for the ProfileUpdateForm.

        Attributes:
            model (class): The Profile model.
            fields (list): The fields to include in the form.
        """
        model = Profile
        fields = ['image', 'phone_number']

    def save(self, commit=True):
        """Saves the profile and processes the phone number.

        Args:
            commit (bool, optional): Indicates whether to commit the changes.
            Default True.

        Returns:
            Profile: The profile object.
        """
        # Call the superclass's save() method to save the form data
        profile = super(ProfileUpdateForm, self).save(commit=False)

        # Process the phone number
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            phone_number_value = phone_number.raw_input

            if phone_number_value[0] == "+":
                phone_number_value = phone_number_value[1:]
            if phone_number_value[0] == "0":
                phone_number_value = "254" + phone_number_value[1:]

            # Save the processed phone number to the profile
            profile.phone_number = phone_number_value

        if commit:
            profile.save()

        return profile
