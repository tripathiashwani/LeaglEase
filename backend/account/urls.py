# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    # path('me/', api.me, name='me'),
    path('user/signup/', signup, name='signup'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/mediator/', register_mediator, name='register_mediator'),
    path('register/lawyer/', register_lawyer, name='register_lawyer'),
    path('register/existing_user_mediator/', register_mediator_for_existing_user, name='register_existing_user_mediator'),

    path('register/lawyer/', register_lawyer, name='register_lawyer'),
]