from django.shortcuts import render

from lists.models import Item


def view_list(request):
    """Представление списка"""
    items = Item.objects.all()
    context = {
        'items': items,
    }
    return render(request=request, template_name='lists/list.html', context=context)
