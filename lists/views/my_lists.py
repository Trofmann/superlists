from django.contrib.auth import get_user_model
from django.shortcuts import render

User = get_user_model()


def my_lists(request, email):
    owner = User.objects.get(email=email)
    context = dict(
        owner=owner,
    )
    return render(request, 'lists/my_lists.html', context)
