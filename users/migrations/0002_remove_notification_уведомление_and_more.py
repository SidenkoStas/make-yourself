# Generated by Django 4.2.3 on 2023-08-01 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='Уведомление',
        ),
        migrations.AddField(
            model_name='notification',
            name='notification',
            field=models.CharField(default=1, max_length=150, verbose_name='Уведомление'),
            preserve_default=False,
        ),
    ]
