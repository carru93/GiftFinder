# Generated by Django 5.0.7 on 2025-01-26 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_notification_notification_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_new_gift',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='email_new_message',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='email_new_review',
            field=models.BooleanField(default=False),
        ),
    ]
