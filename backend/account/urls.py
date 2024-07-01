# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from .api import *

urlpatterns = [
    path('user/profile',ProfileView, name='me'),
    path('user/signup/', signup, name='signup'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/mediator/', register_mediator, name='register_mediator'),
    path('register/lawyer/', register_lawyer, name='register_lawyer'),
    path('register/existing_user_mediator/', register_mediator_for_existing_user, name='register_existing_user_mediator'),
    path('register/lawyer/', register_lawyer, name='register_lawyer'),
    path('send-otp/', SendPhoneOTP.as_view()),
	path('verify-otp/', ValidateOTP.as_view()),
    # password reset
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    # path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    # path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    # path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    # path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    # path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    # path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name=
]