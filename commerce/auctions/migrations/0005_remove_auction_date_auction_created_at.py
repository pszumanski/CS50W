# Generated by Django 5.0.4 on 2024-04-12 10:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auction_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='date',
        ),
        migrations.AddField(
            model_name='auction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
