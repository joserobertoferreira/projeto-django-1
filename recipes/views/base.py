from django.views.generic import ListView

from recipes.models import Recipe


class RecipeBaseListView(ListView):
    model = Recipe
    context_object_name = 'recipes'
    paginate_by = 5
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'
