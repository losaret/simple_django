import pytest
from django.contrib.auth.models import User
from vkusno.models import categories, product_card, status
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username='test_user', password='password')

@pytest.fixture
def test_category(db, test_user):
    return categories.objects.create(
        name="Тестовая категория",
        user=test_user
    )

@pytest.fixture
def test_product_card(db, test_user, test_category):
    image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    return product_card.objects.create(
        user=test_user,
        comment="Тестовая карточка",
        card_image=image,
        choice=status.vkusno,
        category=test_category
    )
