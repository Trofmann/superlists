from django.shortcuts import redirect, render

from ..forms import ItemForm
from ..models import Item, List


def new_list(request):
    """Новый список"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        item = Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    return render(request, 'lists/home.html', {'form': form})
