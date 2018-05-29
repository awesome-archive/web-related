from django.urls import path, re_path
from . import views
from django.contrib.auth.views import login, logout, logout_then_login,\
    password_change, password_change_done,\
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete


# app_name = 'account'
urlpatterns = [
    # root url
    path('', views.dashboard, name='dashboard'),

    # login logout
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('logout-then-login/', logout_then_login, name='logout_then_login'),

    # change password
    path('password-change/', password_change, name='password_change'),
    path('password-change/done/', password_change_done, name='password_change_done'),

    # reset password
    path('password-reset/', password_reset, name='password_reset'),
    path('password-reset/done/', password_reset_done, name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/', password_reset_complete, name='password_reset_complete'),

    # register
    path('register/', views.register, name='register'),

    # edit
    path('edit/', views.edit, name='edit')
]
