from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url('^$', views.home, name='home'),
    url(r"^view/(?P<invoice_id>[\w-]+)/$", views.view_update_invoice, name="view_update_invoice"),
    url(r"^digitize/(?P<invoice_id>[\w-]+)/$", views.digitize_invoice, name="digitize_invoice"),
]
