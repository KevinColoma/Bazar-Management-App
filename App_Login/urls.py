from django.urls import path
from App_Login import views

app_name = 'App_Login'

urlpatterns = [
    path('signup/', views.sign_up, name="signup"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.user_profile, name="profile"),
    path('change-password/', views.change_password, name='change_password'),
    path('all-users/', views.all_users, name="all_users")
]