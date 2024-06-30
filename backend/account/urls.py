# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import LoginView
from .views import signup

urlpatterns = [
    # path('me/', api.me, name='me'),
    path('user/signup/', signup, name='signup'),
    # path('login/', LoginView.as_view(), name='token_obtain'),
    # path('login1/', TokenObtainPairView.as_view(), name='token_obtain'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]