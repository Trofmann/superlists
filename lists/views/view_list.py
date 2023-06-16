from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from lists.models import Item, List


def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            text = request.POST['text']
            item = Item(text=text, list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"
    context = {
        'list': list_,
        'error': error,
    }
    return render(request=request, template_name='lists/list.html', context=context)
