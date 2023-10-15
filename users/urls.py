from django.urls import path
from users.views import CustomTierCreateView

app_name = 'users'

urlpatterns = [
    # Other URL patterns
    path('create-custom-tier/', CustomTierCreateView.as_view(), name='create-custom-tier'),
]