from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import current_user, SignUpView

urlpatterns = [
    path('token/', obtain_jwt_token, name='token'),
    path('signup/', SignUpView.as_view(), name='users'),
    path('current/', current_user, name='current_user'),
]
