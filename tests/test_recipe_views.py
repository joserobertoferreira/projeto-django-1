from http import HTTPStatus

from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_ok(self):  # noqa: PLR6301
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)  # noqa: PT009

    def test_recipe_category_view_function_is_ok(self):  # noqa: PLR6301
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)  # noqa: PT009

    def test_recipe_detail_view_function_is_ok(self):  # noqa: PLR6301
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)  # noqa: PT009

    def test_recipe_home_view_returns_status_code_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)  # noqa: PT009

    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')  # noqa: PT009

    def test_recipe_home_template_shows_not_found_message(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(  # noqa: PT009
            '<h1>Não existem receitas</h1>', response.content.decode('utf-8')
        )
