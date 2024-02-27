# Generated by Django 5.0.1 on 2024-01-22 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hotels",
            fields=[
                ("hotel_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=30)),
                ("address", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=30)),
                ("rating", models.DecimalField(decimal_places=1, max_digits=10)),
                ("amenities", models.CharField(max_length=30)),
            ],
        ),
    ]
