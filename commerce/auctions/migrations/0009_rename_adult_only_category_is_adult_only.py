# Generated by Django 5.0.4 on 2024-04-14 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_rename_active_auction_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='adult_only',
            new_name='is_adult_only',
        ),
    ]