# Generated by Django 3.1.3 on 2021-05-30 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_delete_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-updated_time']},
        ),
    ]
