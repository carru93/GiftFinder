# Generated by Django 5.0.7 on 2024-12-07 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gifts', '0005_gift_suitable_age_range_gift_suitable_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gift',
            name='suitable_age_range',
            field=models.CharField(blank=True, choices=[('0-12', 'Children (0-12)'), ('13-17', 'Teenagers (13-17)'), ('18-24', 'Young Adults (18-24)'), ('25-34', 'Adults (25-34)'), ('35-50', 'Adults (35-50)'), ('50+', 'Seniors (50+)')], max_length=10),
        ),
        migrations.AlterField(
            model_name='gift',
            name='suitable_gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('U', 'Unisex')], max_length=1),
        ),
    ]
