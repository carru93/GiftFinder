# Generated by Django 5.0.7 on 2024-12-07 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0006_alter_gift_suitable_age_range_and_more'),
        ('users', '0005_user_gender_user_location_alter_user_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='possessed_gifts',
            field=models.ManyToManyField(blank=True, related_name='owners', to='gifts.gift'),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Rather not say')], max_length=1),
        ),
    ]
