# Generated by Django 3.0.5 on 2020-08-20 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lunch', '0008_auto_20200817_2348'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ts',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
