from django.contrib import admin
from django.urls import path, include , re_path
from .views import NewUser ,Logout ,Login , MyProfile , Info ,AddUser,Follow

urlpatterns = [
    path('register/', NewUser.as_view()),
    path('login/', Login.as_view()),
    path('profile/', MyProfile.as_view()),
    path('info/<int:id>',Info.as_view()),
    path('add_user/',AddUser.as_view()),
    path('follow/<int:id>',Follow.as_view()),
    path('logout', Logout.as_view()),

]
