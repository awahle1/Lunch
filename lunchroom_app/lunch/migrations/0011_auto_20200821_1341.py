# Generated by Django 3.0.5 on 2020-08-21 17:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lunch', '0010_post_auth_pp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='table',
        ),
        migrations.AddField(
            model_name='post',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='lunch.Table'),
        ),
    ]