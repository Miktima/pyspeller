from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("save_word.html", views.save_word, name='save_word'),
]