"""WebTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path

from WebTest.views import HomeView, ThumbUpView, ThumbDownView, ListThemesView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('home/', HomeView.as_view(), name='home_page'),
    path('video/thumb-up/<slug:id>', ThumbUpView.as_view(), name='video_set_thumb_up'),
    path('video/thumb-down/<slug:id>', ThumbDownView.as_view(), name='video_set_thumb_down'),
    path('video/list-themes/', ListThemesView.as_view(), name='video_list_themes')
]
