# Generated by Django 5.0.7 on 2024-07-26 15:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gifts', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='suggestedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gift',
            name='giftCategories',
            field=models.ManyToManyField(blank=True, to='gifts.giftcategory'),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='gifts',
            field=models.ManyToManyField(to='gifts.gift'),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
