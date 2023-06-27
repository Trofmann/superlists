from django.shortcuts import redirect, render

from ..forms import ItemForm, NewListForm
from ..models import List


def new_list(request):
    """Новый список"""
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(list_)
    return render(request, 'lists/home.html', {'form': form})


def new_list2(request):
    """Новый список 2"""
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'lists/home.html', {'form': form})
