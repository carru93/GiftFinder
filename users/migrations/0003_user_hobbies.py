# Generated by Django 5.0.7 on 2024-08-20 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hobbies', '0003_delete_userhobbies'),
        ('users', '0002_user_public_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hobbies',
            field=models.ManyToManyField(blank=True, related_name='users', to='hobbies.hobby'),
        ),
    ]
