from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_homepage, name="homepage"),
    path("posts/", views.get_posts_page, name="posts-page"),

    path("register/", views.get_register_page, name="register-page"),
    path("login/", views.get_login_page, name="login-page"),
    path("logout/", views.user_logout, name="logout"),

    path("user/<str:username>", views.get_user_profile_page, name="user-profile-page"),
    path("handle-following/<str:username>", views.handle_following, name="handle-following"),

    path("create-post/", views.get_create_post_page, name="create-post"),
    path("post/<str:post_id>/", views.get_post, name="post-page"),
    path("edit-post/<str:post_id>", views.get_edit_post_page, name="edit-post"),
    path("delete-post/<str:post_id>", views.delete_post, name="delete-post"),

    path("like-post/<str:post_id>", views.like_post, name="like-post"),
    path("dislike-post/<str:post_id>", views.dislike_post, name="dislike-post"),
    path("bookmark-post/<str:post_id>", views.bookmark_post, name="bookmark-post"),

    path("like-comment/<str:comment_id>", views.like_comment, name="like-comment"),
    path("dislike-comment/<str:comment_id>", views.dislike_comment, name="dislike-comment"),
    path("delete-comment/<str:comment_id>", views.delete_comment, name="delete-comment"),

    path("followed-users/", views.get_followed_users_page, name="followed-users-page"),
    path("follower-users/", views.get_follower_users_page, name="follower-users-page"),
    path("bookmarked-posts/", views.get_bookmarked_posts_page, name="bookmarked-posts-page"),
    path("liked-posts/", views.get_liked_posts_page, name="liked-posts-page"),
    path("disliked-posts/", views.get_disliked_posts_page, name="disliked-posts-page"),
]