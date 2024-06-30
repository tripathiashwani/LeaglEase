# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import signup

urlpatterns = [
    # path('me/', api.me, name='me'),
    path('user/signup/', signup, name='signup'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]