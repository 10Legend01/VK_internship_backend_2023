from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.users),
    path('users/<int:user_id>/', views.user_detail),
    path('users/<int:user_id>/friends/', views.get_friends),
    path('users/<int:user_id>/friends/in/', views.get_friends_receive),
    path('users/<int:user_id>/friends/out/', views.get_friends_sent),
    path('users/<int:user_id>/friends/<int:friend_id>/', views.friend_status),
    path('users/<int:user_id>/friends/<int:friend_id>/accept/', views.accept_friend_request),
    path('users/<int:user_id>/friends/<int:friend_id>/reject/', views.reject_friend_request),
]
