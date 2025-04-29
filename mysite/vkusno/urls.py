from django.urls import path

from . import views

urlpatterns = [
    path("", views.index.as_view(), name='home'),
    path("post_card/", views.PublishCard.as_view()),
    path("post_category/", views.PublishCategory.as_view()),
    path("upload/", views.image_upload, name="upload"),
    path('card/<int:pk>/delete/', views.DeleteCard.as_view(), name='card_delete'),
]
