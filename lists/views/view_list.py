from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from ..models import Item, List
from ..forms import ItemForm, EMPTY_ITEM_ERROR


def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(list_)
    context = {
        'list': list_,
        'form': form
    }
    return render(request=request, template_name='lists/list.html', context=context)
