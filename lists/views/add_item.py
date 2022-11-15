from django.shortcuts import redirect

from lists.models import List, Item


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    item_data = dict(
        text=request.POST['item_text'],
        list=list_,
    )
    Item.objects.create(**item_data)
    return redirect(f'/lists/{list_.id}/')
