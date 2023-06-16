from django.shortcuts import render, redirect

from ..forms import ItemForm


def home_page(request):
    """Домашняя страница"""
    context = {
        'form': ItemForm()
    }
    return render(request=request, template_name='lists/home.html', context=context)
