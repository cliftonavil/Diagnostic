from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url('', include('lab.urls')),
    url('account/', include('account.urls')),
    # url(r'^signup/', include('accounts.urls')),
    # url(r'^login/', include('accounts.urls')),
]
