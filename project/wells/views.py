from django.shortcuts import render
from .forms import Auth_form


def  index(request):
    auth_form = Auth_form()
    return render(request, 'index.html', {'form': auth_form})
