from django.urls import path

from . import views

urlpatterns = [
    path("", views.index.as_view()),
    path("post/", views.Publishcard.as_view()),
    path("upload/", views.image_upload, name="upload")
]
