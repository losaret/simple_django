import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from vkusno.models import Category, ProductCard, Status


@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="test_user", password="password")


@pytest.fixture
def test_category(db, test_user):
    return Category.objects.create(name="Тестовая категория", user=test_user)


@pytest.fixture
def test_product_card(db, test_user, test_category):
    image = SimpleUploadedFile(
        "test_image.jpg", b"file_content", content_type="image/jpeg"
    )
    return ProductCard.objects.create(
        user=test_user,
        comment="Тестовая карточка",
        card_image=image,
        choice=Status.like,
        category=test_category,
    )


@pytest.fixture(autouse=True)
def media_root(tmp_path, settings):
    test_media_root = tmp_path / "media"
    test_media_root.mkdir()
    settings.MEDIA_ROOT = str(test_media_root)

    yield
