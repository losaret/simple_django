import pytest
from django.urls import reverse
from vkusno.models import categories, product_card
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestHome:
    
    def test_home_authenticated(self, client, test_user):
        """Проверка: авторизованный юзер видит домашнюю страницу."""
        client.force_login(test_user)
        url = reverse('home') 
        response = client.get(url)
        assert response.status_code == 200
        # Проверяем, что в шаблоне используется нужный контекст
        assert 'categories' in response.context

    def test_home_anonymous(self, client):
        """Проверка: неавторизованный юзер перенаправляется на логин."""
        url = reverse('home')
        response = client.get(url)
        assert response.status_code == 302
        assert '/login/' in response.url


@pytest.mark.django_db
class TestCategoryView:

    def test_post_success(self, client, test_user):
        """Проверка: успешное создание новой категории."""
        client.force_login(test_user)
        url = reverse('category_create')
        data = {'name': 'Новая тестовая категория'}
        response = client.post(url, data=data)
        assert response.status_code == 302
        assert categories.objects.filter(user=test_user, name='Новая тестовая категория').exists()

    def test_post_duplicate_ignored(self, client, test_user, test_category):
        """Проверка: дубликат не создает вторую запись."""
        client.force_login(test_user)
        url = reverse('category_create')
        # Пытаемся создать категорию с именем, которое уже есть в фикстуре test_category
        data = {'name': test_category.name}
        # Считаем количество категорий до
        count_before = categories.objects.filter(user=test_user).count()
        response = client.post(url, data=data)
        # Считаем количество после
        count_after = categories.objects.filter(user=test_user).count()
        assert count_after == count_before
        assert response.status_code == 302

    def test_post_anonymous_redirect(self, client):
        """Проверка: анонимный пользователь не может создать категорию."""
        url = reverse('category_create')
        response = client.post(url, data={'name': 'Hack'})
        assert response.status_code == 302
        assert 'login' in response.url

    def test_post_update(self, client, test_user, test_category):
        """Проверка: успешное обновление категории."""
        client.force_login(test_user)
        data = {'name': 'Новое тестовое имя'}
        url = reverse('category_update', kwargs={'pk': test_category.pk})
        response = client.post(url, data=data)
        assert response.status_code == 302
        assert categories.objects.filter(user=test_user, name='Новое тестовое имя').exists()

    def test_post_delete(self, client, test_user, test_category, test_product_card):
        """Проверка: успешное удаление категории."""
        client.force_login(test_user)
        url = reverse('category_delete', kwargs={'pk': test_category.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert categories.objects.count() == 0
        assert product_card.objects.count() == 0


@pytest.mark.django_db
class TestProductCardView:

    def test_post_success(self, client, test_user, test_category):
        """Проверка: успешное создание новой карточки."""
        client.force_login(test_user)
        url = reverse('card_create') 
        gif_data = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded_file = SimpleUploadedFile('test.gif', gif_data, content_type='image/gif')
        data = {
            'comment': 'Новая тестовая карточка',
            'card_image': uploaded_file,
            'choice': 'vk',
            'category': test_category.name
        }
        response = client.post(url, data=data)
        assert response.status_code == 302 
        assert product_card.objects.filter(user=test_user, comment='Новая тестовая карточка').exists()

    def test_post_delete(self, client, test_user, test_category, test_product_card):
        """Проверка: успешное удаление карточки."""
        client.force_login(test_user)
        url = reverse('card_delete', kwargs={'pk': test_product_card.pk})
        response = client.post(url)
        assert response.status_code == 302
        assert product_card.objects.count() == 0

    def test_post_anonymous_redirect(self, client):
        """Проверка: анонимный пользователь не может создать категорию."""
        url = reverse('card_create')
        response = client.post(url, data={'comment': 'Hack'})
        assert response.status_code == 302
        assert 'login' in response.url

