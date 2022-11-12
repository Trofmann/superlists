from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    """Домашняя страница"""
    context = {
        'new_item_text': request.POST.get('item_text', ''),
    }
    return render(request=request, template_name='lists/home.html', context=context)
