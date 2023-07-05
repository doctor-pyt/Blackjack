from django.urls import re_path
from django.contrib import admin
from django.urls import include

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^BJ/", include("BJGame.urls")),
]
