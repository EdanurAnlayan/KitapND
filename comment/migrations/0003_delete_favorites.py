# Generated by Django 3.1.3 on 2021-05-11 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0002_favorites'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorites',
        ),
    ]