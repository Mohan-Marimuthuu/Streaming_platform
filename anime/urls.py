"""
URL configuration for anime project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from tailfox import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('popular/',views.popular,name='popular'),
    path('action/',views.action,name='action'),
    path('account/',views.account,name='account'),
    path('naruto/',views.naruto,name='naruto'),
    path('userData/',views.userData,name='userData'),
    path('login/',views.login,name='login'),
    path("logout/", views.logout, name="logout"),
    path("update-like/<int:anime_id>/", views.update_like, name="update_like"),
    path('search/', views.search, name='search'),
    path('upload_anime/', views.upload_anime, name='upload_anime'),  # create anime
    path('upload_anime/<int:anime_id>/', views.upload_anime, name='upload_anime'), # upload episodes
    path('notifications/', views.notifications, name='notifications'),
    path('anime_detail/<slug:slug>/', views.anime_detail, name='anime_detail'),
    path('add_to_watchlist/<int:anime_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_watchlist/<int:anime_id>/', views.remove_watchlist, name='remove_watchlist'),


    




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
