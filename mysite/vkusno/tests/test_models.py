import pytest
from vkusno.models import categories, product_card
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_category_has_correct_owner(test_category, test_user):
    """
    Тест проверяет, что категория создана и действительно привязана 
    к пользователю, созданному фикстурой.
    """
    assert test_category.pk is not None # Если pk (id) есть, значит, она в БД
    assert categories.objects.filter(name=test_category.name).exists()
    assert test_category.user == test_user
    assert test_category.name == "Тестовая категория"
    assert test_category.user.username == 'test_user'

@pytest.mark.django_db
def test_user_deletion_cascade(test_category, test_user):
    """
    Тест проверяет, что категория удалиться при удалении пользователя
    """
    test_user.delete()
    assert categories.objects.filter(pk=test_category.pk).exists() is False

@pytest.mark.django_db
def test_category_deletion_cascades(test_product_card, test_category, test_user):
        """Проверка: удаление категории удаляет привязанный продукт (CASCADE)."""
        test_category.delete()
        assert product_card.objects.count() == 0