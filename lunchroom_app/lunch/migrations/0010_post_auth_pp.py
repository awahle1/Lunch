# Generated by Django 3.0.5 on 2020-08-20 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lunch', '0009_post_ts'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='auth_pp',
            field=models.CharField(default='', max_length=300),
        ),
    ]
