from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RegisterForm


def register(request):
    register_form_data = request.session.get('register_form_data', None)

    form = RegisterForm(register_form_data)

    return render(
        request,
        'authors/pages/register.html',
        {'form': form, 'form_action': reverse('authors:register_create')},
    )


def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    request.session['register_form_data'] = POST

    form = RegisterForm(POST)

    if form.is_valid():
        # Save the form data to the memory cache
        user = form.save(commit=False)

        user.set_password(user.password)

        # Save the form data to the database
        user.save()

        messages.success(request, 'User created successfully. Please log in.')

        del request.session['register_form_data']
        return redirect(reverse('authors:login'))

    return redirect('authors:register')


def login_view(request):
    form = LoginForm()

    return render(
        request,
        'authors/pages/login.html',
        {'form': form, 'form_action': reverse('authors:login_create')},
    )


def login_create(request):
    if not request.POST:
        raise Http404

    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated:
            messages.success(request, 'Logged.')
            login(request, authenticated)
        else:
            messages.error(request, 'Invalid credentials')
            # Redirect the user to the dashboard
    else:
        messages.error(request, 'Error: Invalid form')

    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request) -> None:
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)

    return redirect(reverse('authors:login'))
