import pytest
from vkusno.forms import PublishCategoryForm, PublishCardForm

def test_publish_category_form():
    """Проверяем, что форма принимает правильные данные."""
    form = PublishCategoryForm(data={'name': 'Тестовая форма'})
    assert form.is_valid() is True