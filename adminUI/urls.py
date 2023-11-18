from django.urls import path
from adminUI import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/',views.UserRegistrationView.as_view(),name="user-registration"),
    path('edituser/<int:id>',views.UserDetailView.as_view(),name="user-edit"),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
]