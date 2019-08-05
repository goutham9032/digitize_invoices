from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static


from app import views as app_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', app_views.login_user, name="login_user"),
    url(r'^accounts/register/$', app_views.register, name="register"),
    url(r'^accounts/logout/$', app_views.logout_user, name='logout_user'),
    url(r'^', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
