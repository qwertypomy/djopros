from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('polls.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
    url("^soc/", include("social.apps.django_app.urls", namespace="social")),
]
