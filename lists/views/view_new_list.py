from django.shortcuts import redirect, render
from django.views.generic import CreateView

from ..forms import NewListForm


class NewListView(CreateView):
    form_class = NewListForm
    template_name = 'lists/home.html'

    def form_valid(self, form):
        list_ = form.save(owner=self.request.user)
        return redirect(list_)
