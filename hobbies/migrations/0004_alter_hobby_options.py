# Generated by Django 5.0.7 on 2024-08-21 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hobbies', '0003_delete_userhobbies'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hobby',
            options={'verbose_name_plural': 'Hobbies'},
        ),
    ]
