"""file_storage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from app.views import (HomePageView, LoginView,
                       logout_user, RegisterView,
                       PersonalArea, upload_handler,
                       download_handler, delete_handler
                       )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', HomePageView.as_view(),name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout$', logout_user, name='logout'),
    url(r'^registration/$', RegisterView.as_view(), name='registration'),
    url(r'^lk/$', PersonalArea.as_view(), name='lk'),
    url(r'^lk/add_file$', upload_handler, name='add-file'),
    url(r'^lk/(?P<pk>[0-9]+)/$', download_handler, name='down-file'),
    url(r'^lk/del_file/(?P<pk>[0-9]+)/$', delete_handler, name='del-file'),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^user/password/reset/$', auth_views.PasswordResetView.as_view(),
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$', auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(),
        {'post_reset_redirect': '/user/password/done/'},
        name="auth_password_reset_confirm"),
    url(r'^user/password/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)