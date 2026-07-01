from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="home"),
    path("about/", views.About.as_view(), name="about"),
    path("post_card/", views.PublishCard.as_view(), name="card_create"),
    path("post_category/", views.PublishCategory.as_view(), name="category_create"),
    path("card/<int:pk>/delete/", views.DeleteCard.as_view(), name="card_delete"),
    path(
        "category/<int:pk>/edit/",
        views.UpdateCategory.as_view(),
        name="category_update",
    ),
    path(
        "category/<int:pk>/delete/",
        views.DeleteCategory.as_view(),
        name="category_delete",
    ),
    path("search/", views.Search.as_view(), name="search"),
    path("<str:username>/", views.OtherProfile.as_view(), name="otherprofile"),
]
