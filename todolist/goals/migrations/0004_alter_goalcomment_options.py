# Generated by Django 4.0.1 on 2023-06-05 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_goalcomment_created_goalcomment_updated'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goalcomment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]