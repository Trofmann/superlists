from django.shortcuts import redirect

from lists.models import Item


def new_list(request):
    """Новый список"""
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/only-one/')
