from django.views.generic import DetailView, CreateView

from ..forms import ExistingListItemForm
from ..models import List


class ViewAndAddToListView(DetailView, CreateView):
    model = List
    template_name = 'lists/list.html'
    form_class = ExistingListItemForm

    def get_form(self, form_class=None):
        self.object = self.get_object()
        return self.form_class(for_list=self.object, data=self.request.POST)
