from django.conf import settings
from django.db import models
from django.urls import reverse


class List(models.Model):
    """
    Список
    """

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
    )

    shared_with = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name='shared_lists',
    )

    def get_absolute_url(self):
        """
        Получение абсолютного url
        """
        return reverse('view_list', args=[self.id])

    @staticmethod
    def create_new(first_item_text, owner=None):
        """Создать новый"""
        list_ = List.objects.create(owner=owner)
        Item.objects.create(text=first_item_text, list=list_)
        return list_

    @property
    def name(self):
        return self.item_set.first().text


class Item(models.Model):
    """
    Элемент списка
    """
    text = models.TextField(default='')
    list = models.ForeignKey(
        to=List,
        default=None,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('view_list', args=[self.list.id])
