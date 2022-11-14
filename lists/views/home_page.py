from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    """Домашняя страница"""
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/only-one/')
    return render(request=request, template_name='lists/home.html')
