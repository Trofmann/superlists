from django.shortcuts import render, redirect

from lists.models import Item, List


def view_list(request, list_id):
    """Представление списка"""
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        text = request.POST['item_text']
        Item.objects.create(text=text, list=list_)
        return redirect(f'/lists/{list_id}/')
    context = {
        'list': list_,
    }
    return render(request=request, template_name='lists/list.html', context=context)
