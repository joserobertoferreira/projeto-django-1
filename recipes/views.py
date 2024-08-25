from django.http import HttpResponse


def home(request):
    return HttpResponse('Welcome to Django')


def about(request):
    return HttpResponse("Hello, world. You're at the about page.")
