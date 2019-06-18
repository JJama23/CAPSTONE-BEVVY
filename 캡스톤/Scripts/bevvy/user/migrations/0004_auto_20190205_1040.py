# Generated by Django 2.1.3 on 2019-02-05 01:40

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', user.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.CharField(blank=True, max_length=20, verbose_name='연령대'),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, max_length=20, verbose_name='성별'),
        ),
    ]
