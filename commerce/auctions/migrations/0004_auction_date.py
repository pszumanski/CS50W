# Generated by Django 5.0.4 on 2024-04-12 10:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auction_category_delete_auctioncategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]