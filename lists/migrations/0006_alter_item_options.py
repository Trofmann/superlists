# Generated by Django 4.0.3 on 2023-06-18 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_alter_item_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
    ]
