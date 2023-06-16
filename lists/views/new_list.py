from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from lists.models import Item, List


def new_list(request):
    """Новый список"""
    list_ = List.objects.create()
    item = Item(text=request.POST['text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'lists/home.html', {'error': error})
    return redirect(list_)
