# Generated by Django 4.1 on 2023-10-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemlist',
            name='itemIsActive',
            field=models.BooleanField(default=True),
        ),
    ]