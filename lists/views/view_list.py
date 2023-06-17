from django.shortcuts import render, redirect

from ..forms import ItemForm
from ..models import List


def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)
    context = {
        'list': list_,
        'form': form
    }
    return render(request=request, template_name='lists/list.html', context=context)
