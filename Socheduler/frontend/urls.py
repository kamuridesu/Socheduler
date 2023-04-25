from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("profile/", views.ProfileView.as_view(), name="frontend_profile"),
    path("posts/", views.PostsView.as_view(), name="frontend_posts"),
    path(
        "posts/delete/<int:pk>",
        views.DeletePostsView.as_view(),
        name="frontend_posts_delete",
    ),
    path(
        "posts/edit/<int:pk>",
        views.EditPostsView.as_view(),
        name="frontend_posts_edit",
    ),
]
