from django.contrib import admin
from django.urls import path
from . import views
from .views import BlogAPIView

urlpatterns = [
    path('', views.toMain, name='home'),
    #path('currentblog', views.toCurrent)
    path('login/', views.toLogin, name='toLogin'),
    path('blog/<int:blog_id>/', views.toCurrent, name='current_blog'),
    path('api/v1/bloglist/', BlogAPIView.as_view()),
    path('api/v1/bloglist/<int:pk>/', BlogAPIView.as_view()),
    path('google-auth/', views.google_auth, name='google_auth'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('logout/', views.toLogout, name='logout'),
]
