from django.urls import path, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    path(r'^signup/$', views.signup_view, name='signup'),
    path(r'^login/$', views.login_view, name='login'),
]