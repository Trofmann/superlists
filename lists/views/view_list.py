from django.shortcuts import render, redirect

from ..forms import ItemForm, ExistingListItemForm
from ..models import List


def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    context = {
        'list': list_,
        'form': form
    }
    return render(request=request, template_name='lists/list.html', context=context)
