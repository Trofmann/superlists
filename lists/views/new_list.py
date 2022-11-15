from django.shortcuts import redirect

from lists.models import Item, List


def new_list(request):
    """Новый список"""
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
