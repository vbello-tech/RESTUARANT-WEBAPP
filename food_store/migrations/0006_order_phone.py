# Generated by Django 4.0.6 on 2022-07-08 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_store', '0005_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
