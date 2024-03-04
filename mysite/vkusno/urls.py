from django.urls import path

from . import views

urlpatterns = [
    path("", views.index.as_view(), name='home'),
    path("post_card/", views.Publishcard.as_view()),
    path("post_category/", views.Publishcategory.as_view()),
    path("upload/", views.image_upload, name="upload")
]
