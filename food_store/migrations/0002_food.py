# Generated by Django 4.0.6 on 2022-07-08 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Snacks', 'Snacks'), ('Drinks', 'Drinks'), ('Coffee', 'Coffee'), ('Desert', 'Desert')], max_length=200)),
                ('img', models.ImageField(blank=True, upload_to='FOOD/')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=750)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dis_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('label', models.CharField(blank=True, choices=[('Local Delicacies', 'Local Delicacies'), ('Foriegn Delicacies', 'Foriegn Delicacies'), ('Medicinal Drinks', 'Medicinal Drinks'), ('Wines & Alcohol', 'Wines & Alcohol')], max_length=100, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
