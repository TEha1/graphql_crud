# Generated by Django 3.2.19 on 2023-05-09 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'pending'), (2, 'on delivery'), (3, 'delivered'), (4, 'cancelled')], default=1),
        ),
    ]