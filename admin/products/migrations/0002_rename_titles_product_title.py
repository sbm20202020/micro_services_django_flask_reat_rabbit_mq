# Generated by Django 4.0 on 2021-12-31 06:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='titles',
            new_name='title',
        ),
    ]
