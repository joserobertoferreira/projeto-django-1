from http import HTTPStatus

from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeBaseTest


class RecipeViewsTest(RecipeBaseTest):
    def test_recipe_home_view_function_is_ok(self):  # noqa: PLR6301
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)  # noqa: PT009

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

    def test_recipe_home_template_load_recipes(self):
        self.create_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        recipe_context = response.context['recipes']

        self.assertIn('Title', content)  # noqa: PT009
        self.assertEqual(len(recipe_context), 1)  # noqa: PT009

    def test_recipe_home_template_not_published(self):
        self.create_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(  # noqa: PT009
            '<h1>Não existem receitas</h1>', response.content.decode('utf-8')
        )

    def test_recipe_category_view_function_is_ok(self):  # noqa: PLR6301
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)  # noqa: PT009

    def test_recipe_category_view_returns_status_code_NOT_FOUND(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # noqa: PT009

    def test_recipe_category_template_load_recipes(self):
        test_title = 'Category Page'
        self.create_recipe(title=test_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(test_title, content)  # noqa: PT009

    def test_recipe_category_template_not_published(self):
        recipe = self.create_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:category', kwargs={'category_id': recipe.category_id}
            )
        )

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)  # noqa: PT009

    def test_recipe_detail_view_function_is_ok(self):  # noqa: PLR6301
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)  # noqa: PT009

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
