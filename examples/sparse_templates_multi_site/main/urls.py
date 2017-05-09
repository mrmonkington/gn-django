from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view()),
    url(r'^article', views.Article.as_view()),
]

