from django.shortcuts import redirect, render

from ..forms import NewListForm


def new_list(request):
    """Новый список"""
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'lists/home.html', {'form': form})
