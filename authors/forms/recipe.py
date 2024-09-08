from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from resources.utils.django_forms import add_attribute


class AuthorsRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._errors = defaultdict(list)

        add_attribute(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = [
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'cover',
        ]
        widgets = {
            'cover': forms.FileInput(attrs={'class': 'span-2'}),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Unidade', 'Unidade'),
                    ('Pedaço', 'Pedaço'),
                    ('Litros', 'Litros'),
                    ('Fatias', 'Fatias'),
                    ('Pessoas', 'Pessoas'),
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas'),
                )
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)

        clean_data = self.clean_data

        title = clean_data.get('title')

        if len(title) < 5:  # noqa: PLR2004
            self._errors['title'].append(
                'Título precisa ter no mínimo 5 caracteres',
                code='title_too_short',
            )

        if self._errors:
            raise ValidationError(self._errors)

        return super_clean

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if len(description) < 20:  # noqa: PLR2004
            self._errors['description'].append(
                'Descrição precisa ter no mínimo 20 caracteres',
                code='description_too_short',
            )

        return description
