# Generated by Django 4.0.6 on 2022-07-09 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_store', '0008_alter_food_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snacks', 'Snacks'), ('Drinks', 'Drinks'), ('Coffee', 'Coffee'), ('Desert', 'Desert')], max_length=200),
        ),
    ]
