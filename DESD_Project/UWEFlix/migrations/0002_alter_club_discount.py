# Generated by Django 3.2.16 on 2023-03-30 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlix', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='discount',
            field=models.IntegerField(),
        ),
    ]
