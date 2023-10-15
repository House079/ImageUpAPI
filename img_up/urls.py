from django.urls import path
from .views import (ImageListAPIView,
                    ImageCreateAPIView,
                    ExpiringLinkListCreateAPIView,
                    ExpiringLinkDetailAPIView
                    )

app_name = 'img_up'

urlpatterns = [
    path('upload/', ImageCreateAPIView.as_view(), name='upload_image'),
    path('', ImageListAPIView.as_view(), name='image_list_api'),
    path('expiring-link/', ExpiringLinkListCreateAPIView.as_view(), name='expiring_link'),
    path('expiring-link/<str:signed_link>/', ExpiringLinkDetailAPIView.as_view(), name='expiring_link_detail')
]
