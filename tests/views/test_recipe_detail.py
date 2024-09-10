from http import HTTPStatus

from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeBaseTest


class DetailViewsTest(RecipeBaseTest):
    def test_recipe_detail_view_function_is_ok(self):  # noqa: PLR6301
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        assert view.func.view_class is views.DetailView

    def test_recipe_detail_view_returns_status_code_NOT_FOUND(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # noqa: PT009

    def test_recipe_detail_template_load_recipe(self):
        test_title = 'Detail Page - Read one recipe'
        self.create_recipe(title=test_title)

        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        content = response.content.decode('utf-8')

        self.assertIn(test_title, content)  # noqa: PT009

    def test_recipe_detail_template_not_published(self):
        recipe = self.create_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # noqa: PT009
