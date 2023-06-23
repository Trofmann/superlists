from django.shortcuts import render


def my_lists(request, email):
    return render(request, 'lists/my_lists.html')
