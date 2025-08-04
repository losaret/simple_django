from django.urls import path

from . import views

urlpatterns = [
    path("", views.Index.as_view(), name='home'),
    path("post_card/", views.PublishCard.as_view()),
    path("post_category/", views.PublishCategory.as_view()),
    path("upload/", views.image_upload, name="upload"),
    path('card/<int:pk>/delete/', views.DeleteCard.as_view(), name='card_delete'),
    path('category/<int:pk>/edit/', views.UpdateCategory.as_view(), name='category_edit'),
    path('category/<int:pk>/delete/', views.DeleteCategory.as_view(), name='category_delete')
]
