from django.shortcuts import render

from lists.models import Item, List


def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    context = {
        'list': list_,
    }
    return render(request=request, template_name='lists/list.html', context=context)
