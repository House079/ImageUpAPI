from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser  # Import your custom user model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'tier')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'tier')
