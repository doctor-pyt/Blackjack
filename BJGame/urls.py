from django.urls import re_path
from . import views_nocls

urlpatterns = [
    re_path(r"^Game/$", views_nocls.game, name="game"),
    re_path(r"^howto/$", views_nocls.howto),
]
