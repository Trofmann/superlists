from django.shortcuts import redirect

from lists.models import List


def share_list(request, list_id):
    """Поделиться"""
    list_ = List.objects.get(id=list_id)
    if request.method == 'POST':
        email = request.POST['sharee']
        list_.shared_with.add(email)
    return redirect(list_)
