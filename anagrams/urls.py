from django.urls import path

from . import views

app_name = 'anagrams'

urlpatterns= [
    path ('', views.home, name='home'),
    path ('past_anagrams/', views.past_anagrams, name='past anagrams'),
    path ('solve/<int:anagram_id>/', views.check_solution, name='check solution'),
    path ('solution/<int:anagram_id>/', views.reveal_solution, name='reveal solution'),
    path ('detail/<int:anagram_id>/', views.detail, name='detail'),
    path ('login_page/', views.login_page, name='login page'),
    path ('signup_page/', views.signup_page, name='signup page'),
    path ('logout/', views.logout_view, name='logout'),
    path ('login/', views.login_view, name='login'),
    path ('create_user/', views.create_user, name='create user'),
    path ('post_comment/<int:anagram_id>/', views.post_comment, name='post comment'),
    path ('like_comment/<int:comment_id>/', views.like_comment, name='like comment'),
    path ('delete_comment/<int:comment_id>/', views.delete_comment, name='delete comment'),
    path ('create_anagram/', views.create_anagram, name='create anagram'),
    path ('create_anagram_page/', views.create_anagram_page, name='create anagram page'),
    path ('profile/<int:user_id/', views.profile_page, name='profile page'),
    path ('about_page/', views.about_page, name='about page'),
    path ('monthly_leaderboard/', views.leaderboard, name='monthly leaderboard')

]