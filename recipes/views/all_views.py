import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from recipes.models import Recipe
from resources.utils.pagination import pagination

PER_PAGE = int(os.getenv('PER_PAGE', 6))  # noqa: PLW1508


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/home.html',
        context={'recipes': page_obj, 'pagination_range': pagination_range},
    )


def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(
        request,
        'recipes/pages/recipe-view.html',
        context={'recipe': recipe, 'is_detail_page': True},
    )


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, is_published=True
        ).order_by('-id')
    )

    page_obj, pagination_range = pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'title': f'Categoria - {recipes[0].category.name} |',
        },
    )


def search(request):
    search_term = request.GET.get('search', '').strip()

    if not search_term:
        raise Http404

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term)
            | Q(description__icontains=search_term)
        ),
        is_published=True,
    ).order_by('-id')

    page_obj, pagination_range = pagination(request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/search.html',
        {
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'recipes': page_obj,
            'pagination_range': pagination_range,
            'url_query': f'&search={search_term}',
        },
    )
