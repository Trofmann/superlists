from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    """Домашняя страница"""
    return render(request=request, template_name='lists/home.html')
