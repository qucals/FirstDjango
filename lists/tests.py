from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve

from lists.views import home_page


class HomePageTest(TestCase):
    """
    Тест домашней страницы
    """

    def test_root_url_resolves_to_home_page_view(self):
        """
        Тест: корневой url преобразуется в представление
        домашней страницы
        """

        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_connect_html(self):
        """
        Тест: домашняя страница возвращает правильный html
        """

        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))

    def test_uses_home_template(self):
        """
        Тест: используется домашний шаблон
        """

        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_post_request(self):
        """
        Тест: можно сохранить post-запрос
        """

        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')