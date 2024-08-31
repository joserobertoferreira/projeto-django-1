from http import HTTPStatus

from django.urls import resolve, reverse

from recipes import views
from tests.test_recipe_base import RecipeBaseTest


class CategoryViewsTest(RecipeBaseTest):
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
