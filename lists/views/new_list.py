from django.shortcuts import redirect, render

from ..forms import ItemForm
from ..models import List


def new_list(request):
    """Новый список"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    return render(request, 'lists/home.html', {'form': form})
