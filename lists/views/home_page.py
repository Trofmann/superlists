from django.views.generic import FormView

from ..forms import ItemForm


class HomePageView(FormView):
    """Домашняя страница"""
    template_name = 'lists/home.html'
    form_class = ItemForm
