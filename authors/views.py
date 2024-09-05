from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from authors.forms import RegisterForm


def register(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)

    return render(
        request,
        'authors/pages/register.html',
        {
            'form': form,
        },
    )


def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['register_form_data'] = POST

    form = RegisterForm(POST)

    if form.is_valid():
        # Save the form data to the database
        form.save()
        messages.success(request, 'User created successfully.')

        del request.session['register_form_data']

    return redirect('authors:register')
