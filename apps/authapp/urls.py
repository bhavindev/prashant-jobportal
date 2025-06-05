from django.urls import path
from apps.authapp.views import *

urlpatterns = [
    path('admin/users', usersList, name='users'),
    path('admin/user/create', createUser, name="createUser"),
    path('admin/edit-profile/<slug:slug>/', editUserProfile, name='editProfile'),
    path('admin/change-password/<str:username>/', changePassword, name='change_password'),
    path('admin/users/delete/<str:username>/', delete_user, name='delete_user'),
    path('admin/user/profile', userProfile, name='Userprofile'),
    path('sign-in/', signIn , name='signIn'),
    path('sign-up/', SignUp , name='signUp'),
    path('log-out/', logout_view, name='logOut'),

    path('forgot-password/', initiate_password_reset, name='initiate_password_reset'),
    path('reset_password/<uuid:token>/', reset_password, name='reset_password'),
]
