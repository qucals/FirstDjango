from django.test import TestCase
from django.urls import resolve

from lists.views import home_page
from lists.models import Item


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

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_aster_post(self):
        """
        Тест: переадресует после post-запроса
        """

        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/.../')

    def test_only_saves_items_with_necessary(self):
        """
        Тест: сохраняет элементы, только когда нужно
        """

        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    """
    Тест модели элемента списка
    """

    def test_saving_and_retrieving_items(self):
        """
        Тест сохранения и получения элементов списка
        """

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):
    """
    Тест представления спика
    """

    def test_uses_list_template(self):
        """
        Тест: используется шаблон списка
        """

        response = self.client.get('/lists/.../')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        """
        Тест: отображаются все элементы списка
        """

        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/.../')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
