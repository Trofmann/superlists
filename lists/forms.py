from django import forms
from django.core.exceptions import ValidationError

from .models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"


class ItemForm(forms.ModelForm):
    """Форма элемента списка"""

    class Meta:
        model = Item
        fields = (
            'text',
        )
        widgets = {
            'text': forms.TextInput(
                attrs={
                    'placeholder': 'Enter a to-do item',
                    'class': 'form-control input-lg',
                }
            )
        }
        error_messages = {
            'text': {
                'required': EMPTY_ITEM_ERROR
            }
        }


class NewListForm(ItemForm):
    """Форма для нового списка"""

    def save(self, owner):
        create_kwargs = dict(first_item_text=self.cleaned_data['text'])
        if owner.is_authenticated:
            create_kwargs.update(owner=owner)
        return List.create_new(**create_kwargs)


class ExistingListItemForm(ItemForm):
    """Форма элемента списка для уже существующего списка"""

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {
                'text': [DUPLICATE_ITEM_ERROR]
            }
            self._update_errors(e)
